// selector 选股器，自动按条件筛选优质公司。（好公司，但不代表当前股价在涨）
// 筛选规则：
// 行业要分散
// 最新 ROE 高于 8%
// ROE 平均值小于 20 时，至少 3 年内逐年递增
// EPS 至少 3 年内逐年递增
// 营业总收入至少 3 年内逐年递增
// 净利润至少 3 年内逐年递增
// 估值较低或中等
// 股价低于合理价格
// 负债率低于 60%

package core

import (
	"context"
	"fmt"
	"math"
	"sync"

	"github.com/axiaoxin-com/investool/datacenter"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/logging"
	"github.com/spf13/viper"
	"go.uber.org/zap"
)

// Selector 选股器
type Selector struct {
	Filter  eastmoney.Filter
	Checker *Checker
}

// NewSelector 创建选股器
func NewSelector(ctx context.Context, filter eastmoney.Filter, checker *Checker) Selector {
	return Selector{
		Filter:  filter,
		Checker: checker,
	}
}

// AutoFilterStocks 按默认设置自动筛选股票
func (s Selector) AutoFilterStocks(ctx context.Context) (result models.StockList, err error) {
	stocks, err := datacenter.EastMoney.QuerySelectedStocksWithFilter(ctx, s.Filter)
	if err != nil {
		return
	}
	logging.Infof(ctx, "AutoFilterStocks will filter from %d stocks by %s", len(stocks), s.Filter.String())
	if len(stocks) == 0 {
		return
	}

	// 并发执行筛选任务
	workerCount := int(math.Min(float64(len(stocks)), float64(viper.GetFloat64("app.chan_size"))))
	jobChan := make(chan struct{}, workerCount)
	wg := sync.WaitGroup{}
	var mu sync.Mutex

	for _, baseInfo := range stocks {
		wg.Add(1)
		jobChan <- struct{}{}

		go func(ctx context.Context, baseInfo eastmoney.StockInfo) {
			defer func() {
				wg.Done()
				<-jobChan
				if r := recover(); r != nil {
					logging.Errorf(ctx, "recover from:%v", r)
				}
			}()

			stock, err := models.NewStock(ctx, baseInfo)
			if err != nil {
				logging.Error(ctx, "NewStock error:"+err.Error())
				return
			}
			if s.Checker == nil {
				mu.Lock()
				result = append(result, stock)
				mu.Unlock()
			} else {
				// 检测是否为优质股票
				if details, ok := s.Checker.CheckFundamentals(ctx, stock); ok {
					mu.Lock()
					result = append(result, stock)
					mu.Unlock()
				} else {
					logging.Debug(ctx, fmt.Sprintf("%s %s has some defects", stock.BaseInfo.SecurityNameAbbr, stock.BaseInfo.Secucode), zap.Any("details", details))
				}
			}
		}(ctx, baseInfo)
	}
	wg.Wait()
	logging.Infof(ctx, "AutoFilterStocks selected %d stocks", len(result))
	result.SortByROE()
	return
}
