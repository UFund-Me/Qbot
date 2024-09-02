// 天天基金净值列表

package eastmoney

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/avast/retry-go"
	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/corpix/uarand"
	"github.com/spf13/viper"
	"go.uber.org/zap"
)

// FundType 基金类型
type FundType int

const (
	// 基金类型定义

	// FundTypeALL 全部
	FundTypeALL FundType = 0
	// FundTypeStock 股票型
	FundTypeStock FundType = 25
	// FundTypeMix 混合型
	FundTypeMix FundType = 27
	// FundTypeIndex 指数型
	FundTypeIndex FundType = 26
	// FundTypeBond 债券型
	FundTypeBond FundType = 31
	// FundTypeCurrency 货币型
	FundTypeCurrency FundType = 35
	// FundTypeFOF FOF型
	FundTypeFOF FundType = 15
	// FundTypeQDII QDII型
	FundTypeQDII FundType = 6
	// FundTypeETF ETF
	FundTypeETF FundType = 3
	// FundTypeETFLink ETF联接
	FundTypeETFLink FundType = 33
	// FundTypeLOF LOF
	FundTypeLOF FundType = 4
	// FundTypeDealMoney 理财
	FundTypeDealMoney FundType = 2949
)

// FundListItem RespFundNetList Datas 列表元素
type FundListItem struct {
	// 基金代码
	Fcode string `json:"FCODE"`
	// 基金名
	Shortname string `json:"SHORTNAME"`
	// 001:股票型、指数型、ETF、ETF联接、LOF
	// 002:混合型、FOF
	// 003:债券型
	// 005:货币型
	// 007:QDII型
	Fundtype  string `json:"FUNDTYPE"`
	Bfundtype string `json:"BFUNDTYPE"`
	Feature   string `json:"FEATURE"`
	Fsrq      string `json:"FSRQ"`
	Gpsj      string `json:"GPSJ"`
	// 净值
	Zjl         string `json:"ZJL"`
	Opendate    string `json:"OPENDATE"`
	Targetyield string `json:"TARGETYIELD"`
	Dwjz        string `json:"DWJZ"`
	Hldwjz      string `json:"HLDWJZ"`
	Ljjz        string `json:"LJJZ"`
	// 日涨幅 (%)
	Rzdf    string `json:"RZDF"`
	Cycle1  string `json:"CYCLE1"`
	Isbuy   string `json:"ISBUY"`
	Bagtype string `json:"BAGTYPE"`
	// 可申购状态
	Sgzt        string `json:"SGZT"`
	Buy         bool   `json:"BUY"`
	Listtexch   string `json:"LISTTEXCH"`
	Islisttrade string `json:"ISLISTTRADE"`
}

// FundList 基金列表
type FundList []FundListItem

// RespFundList 净值列表接口原始返回结构
type RespFundList struct {
	Datas        []FundList  `json:"Datas"`
	ErrCode      int         `json:"ErrCode"`
	Success      bool        `json:"Success"`
	ErrMsg       interface{} `json:"ErrMsg"`
	Message      interface{} `json:"Message"`
	ErrorCode    string      `json:"ErrorCode"`
	ErrorMessage interface{} `json:"ErrorMessage"`
	ErrorMsgLst  interface{} `json:"ErrorMsgLst"`
	TotalCount   int         `json:"TotalCount"`
	Expansion    []string    `json:"Expansion"`
}

// QueryAllFundList 获取天天基金净值列表全量数据，耗时很长
func (e EastMoney) QueryAllFundList(ctx context.Context, fundType FundType) (FundList, error) {
	resp, err := e.QueryFundListByPage(ctx, fundType, 1)
	if err != nil {
		return nil, err
	}

	result := FundList{}
	if len(resp.Datas) == 0 {
		return result, nil
	}
	totalCount := resp.TotalCount
	// 首页数据
	result = append(result, resp.Datas[0]...)

	// 算出总页数循环获取全量数据
	pageCount := (totalCount + 30 - 1) / 30
	chanSize := viper.GetInt("app.chan_size")
	reqChan := make(chan int, chanSize)
	var mu sync.Mutex
	var wg sync.WaitGroup
	var sm sync.Map

	wg.Add(pageCount - 1)
	for pageIndex := 2; pageIndex <= pageCount; pageIndex++ {
		reqChan <- pageIndex
		go func() {
			defer func() {
				wg.Done()
			}()
			index := <-reqChan
			resp := RespFundList{}
			err := retry.Do(
				func() error {
					var err error
					resp, err = e.QueryFundListByPage(ctx, fundType, index)
					return err
				},
				retry.OnRetry(func(n uint, err error) {
					logging.Debugf(ctx, "retry#%d: page:%v %v", n, index, err)
				}),
				retry.Attempts(3),
				retry.Delay(300*time.Millisecond),
			)
			if err != nil {
				logging.Errorf(ctx, "QueryAllFundList QueryFundListByPage:%d err:%v", index, err)
				return
			}
			if len(resp.Datas) != 0 {
				for _, d := range resp.Datas[0] {
					if _, exist := sm.Load(d.Fcode); exist {
						logging.Debugf(ctx, "code:%v is already exist", d.Fcode)
						continue
					}
					mu.Lock()
					result = append(result, d)
					mu.Unlock()
					sm.Store(d.Fcode, struct{}{})
				}
			}
		}()
	}
	wg.Wait()

	if len(result) != totalCount {
		logging.Errorf(ctx, "QueryAllFundList result count:%d != resp.TotalCount:%d", len(result), totalCount)
	}
	return result, nil
}

// QueryFundListByPage 按页获取天天基金净值列表，接口限制最大30个
func (e EastMoney) QueryFundListByPage(ctx context.Context, fundType FundType, pageIndex int) (RespFundList, error) {
	apiurl := "http://fundmobapi.eastmoney.com/FundMNewApi/FundMNNetNewList"
	params := map[string]string{
		"FundType":   fmt.Sprint(fundType), // 基金类型
		"SortColumn": "RZDF",               // 按净值排序
		"Sort":       "desc",               // 降序排列
		"pageIndex":  fmt.Sprint(pageIndex),
		"pageSize":   "30",
		"plat":       "Iphone",
		"deviceid":   fmt.Sprint(time.Now().UnixNano()),
		"product":    "EFund",
		"version":    "6.4.5",
	}
	logging.Debug(ctx, "EastMoney QueryFundListByPage "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return RespFundList{}, err
	}
	resp := RespFundList{}
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFundListByPage "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return resp, err
	}
	if resp.ErrCode != 0 {
		return resp, fmt.Errorf("QueryFundListByPage ErrCode != 0: %+v", resp)
	}
	if resp.ErrCode == 0 && len(resp.Datas) == 0 {
		return resp, fmt.Errorf("QueryFundListByPage ErrCode == 0 but not data: %+v", resp)
	}
	return resp, nil
}
