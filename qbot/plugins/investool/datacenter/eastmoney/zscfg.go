// 指数成分股

package eastmoney

import (
	"context"
	"fmt"

	"github.com/axiaoxin-com/goutils"
	"github.com/corpix/uarand"
)

// ZSCFGItem 指数成分股信息
type ZSCFGItem struct {
	IndexCode    string `json:"IndexCode"`    // 指数代码
	IndexName    string `json:"IndexName"`    // 指数名称
	StockCode    string `json:"StockCode"`    // 股票代码
	StockName    string `json:"StockName"`    // 股票名称
	Snewprice    string `json:"SNEWPRICE"`    // 最新价格
	Snewchg      string `json:"SNEWCHG"`      // 最新涨幅
	Marketcappct string `json:"MARKETCAPPCT"` // 持仓比例（%）
	StockTEXCH   string `json:"StockTEXCH"`
	Dctexch      string `json:"DCTEXCH"`
}

// RspZSCFG ZSCFG接口返回结构
type RspZSCFG struct {
	Datas        []ZSCFGItem `json:"Datas"`
	ErrCode      int         `json:"ErrCode"`
	Success      bool        `json:"Success"`
	ErrMsg       interface{} `json:"ErrMsg"`
	Message      interface{} `json:"Message"`
	ErrorCode    string      `json:"ErrorCode"`
	ErrorMessage interface{} `json:"ErrorMessage"`
	ErrorMsgLst  interface{} `json:"ErrorMsgLst"`
	TotalCount   int         `json:"TotalCount"`
	Expansion    interface{} `json:"Expansion"`
}

// ZSCFG 返回指数成分股列表
func (e EastMoney) ZSCFG(ctx context.Context, indexCode string) (results []ZSCFGItem, err error) {
	apiurl := fmt.Sprintf(
		"https://fundztapi.eastmoney.com/FundSpecialApiNew/FundSpecialZSB30ZSCFG?IndexCode=%s&Version=6.5.5&deviceid=-&pageIndex=1&pageSize=10000&plat=Iphone&product=EFund",
		indexCode,
	)
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	rsp := RspZSCFG{}
	if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, &rsp); err != nil {
		return nil, err
	}
	if rsp.ErrCode != 0 {
		return nil, fmt.Errorf("ZSCFG rsp code error, rsp:%+v", rsp)
	}
	if len(rsp.Datas) != rsp.TotalCount {
		return nil, fmt.Errorf("ZSCFG rsp data len:%d != TotalCount:%d", len(rsp.Datas), rsp.TotalCount)
	}
	return rsp.Datas, nil
}
