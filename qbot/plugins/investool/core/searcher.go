// 关键词搜索股票

package core

import (
	"context"
	"errors"
	"fmt"
	"math"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/avast/retry-go"
	"github.com/axiaoxin-com/investool/datacenter"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/investool/datacenter/sina"
	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/logging"
	"github.com/spf13/viper"
)

// Searcher 搜索器实例
type Searcher struct{}

// NewSearcher 创建搜索器实例
func NewSearcher(ctx context.Context) Searcher {
	return Searcher{}
}

// SearchStocks 按股票名或代码搜索股票
func (s Searcher) SearchStocks(ctx context.Context, keywords []string) (map[string]models.Stock, error) {
	var wg sync.WaitGroup
	var mu sync.Mutex
	kLen := len(keywords)
	if kLen == 0 {
		return nil, errors.New("empty keywords")
	}
	// 根据关键词匹配股票代码
	matchedResults := []sina.SearchResult{}
	for _, kw := range keywords {
		wg.Add(1)
		go func(kw string) {
			defer func() {
				wg.Done()
			}()
			searchResults, err := datacenter.Sina.KeywordSearch(ctx, kw)
			if err != nil {
				logging.Errorf(ctx, "search %s error:%s", kw, err.Error())
				return
			}
			if len(searchResults) == 0 {
				logging.Warnf(ctx, "search %s no data", kw)
				return
			}
			logging.Infof(ctx, "search keyword:%s results:%+v, %+v matched", kw, searchResults, searchResults[0])
			mu.Lock()
			matchedResults = append(matchedResults, searchResults[0])
			mu.Unlock()
		}(kw)
	}
	wg.Wait()
	if len(matchedResults) == 0 {
		return nil, fmt.Errorf("无法获取对应数据 %v", keywords)
	}
	// 查询匹配到的股票代码的股票信息
	filter := eastmoney.Filter{}
	for _, result := range matchedResults {
		filter.SpecialSecurityCodeList = append(filter.SpecialSecurityCodeList, result.SecurityCode)
	}
	stocks, err := datacenter.EastMoney.QuerySelectedStocksWithFilter(ctx, filter)
	if err != nil {
		return nil, err
	}
	results := map[string]models.Stock{}
	for _, stock := range stocks {
		wg.Add(1)
		go func(stock eastmoney.StockInfo) {
			defer func() {
				wg.Done()
			}()
			mstock, err := models.NewStock(ctx, stock)
			if err != nil {
				logging.Errorf(ctx, "%s new models stock error:%v", stock.SecurityCode, err.Error())
				return
			}
			mu.Lock()
			results[stock.SecurityCode] = mstock
			mu.Unlock()
		}(stock)
	}
	wg.Wait()
	return results, nil
}

// SearchFunds 按基金代码搜索基金
func (s Searcher) SearchFunds(ctx context.Context, fundCodes []string) (map[string]*models.Fund, error) {
	codeLen := len(fundCodes)
	if codeLen == 0 {
		return nil, errors.New("empty fund codes")
	}
	start := time.Now()
	workerCount := int(math.Min(float64(codeLen), viper.GetFloat64("app.chan_size")))
	logging.Infof(ctx, "SearchFunds request start... workerCount=%d", workerCount)

	reqChan := make(chan string, workerCount)
	result := map[string]*models.Fund{}
	var wg sync.WaitGroup
	var mu sync.Mutex
	for _, code := range fundCodes {
		if strings.TrimSpace(code) == "" {
			continue
		}
		matched, err := regexp.MatchString(`\d{6}`, code)
		if err != nil {
			logging.Errorf(ctx, "SearchFunds match code:%v err:%v", code, err)
			continue
		}
		if !matched {
			continue
		}
		wg.Add(1)
		reqChan <- code
		go func() {
			defer func() {
				wg.Done()
			}()

			code := <-reqChan
			fundresp := &eastmoney.RespFundInfo{}
			err := retry.Do(
				func() error {
					var err error
					fundresp, err = datacenter.EastMoney.QueryFundInfo(ctx, code)
					return err
				},
				retry.OnRetry(func(n uint, err error) {
					logging.Debugf(ctx, "retry#%d: code:%v %v", n, code, err)
				}),
				retry.Attempts(3),
				retry.Delay(500*time.Millisecond),
			)
			if err != nil {
				logging.Errorf(ctx, "SearchFunds QueryFundInfo code:%v err:%v", code, err)
				return
			}
			fund := models.NewFund(ctx, fundresp)
			mu.Lock()
			result[fund.Code] = fund
			mu.Unlock()
		}()
	}
	wg.Wait()
	logging.Infof(ctx, "SearchFunds request end. latency:%+v", time.Now().Sub(start))
	return result, nil
}

// SearchFundByStock 根据股票名称查询持有该股票的基金
func (s Searcher) SearchFundByStock(ctx context.Context, stockNames ...string) ([]eastmoney.HoldStockFund, error) {
	var wg sync.WaitGroup
	var mu sync.Mutex
	kLen := len(stockNames)
	if kLen == 0 {
		return nil, errors.New("empty stockNames")
	}
	// 基金出现次数统计：key=基金代码 value=出现次数
	countMap := map[string]int{}
	fundMap := map[string]eastmoney.HoldStockFund{}
	for _, kw := range stockNames {
		wg.Add(1)
		go func(kw string) {
			defer func() {
				wg.Done()
			}()
			searchResults, err := datacenter.Sina.KeywordSearch(ctx, kw)
			if err != nil {
				logging.Errorf(ctx, "search %s error:%s", kw, err.Error())
				return
			}
			if len(searchResults) == 0 {
				logging.Warnf(ctx, "search %s no data", kw)
				return
			}
			logging.Infof(ctx, "search keyword:%s results:%+v, %+v matched", kw, searchResults, searchResults[0])
			result := searchResults[0]
			holdStockFunds, err := datacenter.EastMoney.QueryFundByStock(ctx, result.Name, result.SecurityCode)
			if err != nil {
				logging.Error(ctx, "SearchFundByStock QueryFundByStock err:"+err.Error())
			}
			mu.Lock()
			for _, f := range holdStockFunds {
				countMap[f.Fcode] = countMap[f.Fcode] + 1
				fundMap[f.Fcode] = f
			}
			mu.Unlock()
		}(kw)
	}
	wg.Wait()

	stockCount := len(stockNames)
	results := []eastmoney.HoldStockFund{}
	for fcode, count := range countMap {
		if count == stockCount {
			results = append(results, fundMap[fcode])
		}
	}
	logging.Infof(ctx, "SearchFundByStock with %v has %d results", stockNames, len(results))
	return results, nil
}
