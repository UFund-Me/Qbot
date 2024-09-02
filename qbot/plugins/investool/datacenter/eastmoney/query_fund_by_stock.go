// 天天基金根据股票查询基金

package eastmoney

import (
	"context"
	"fmt"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/corpix/uarand"
	"go.uber.org/zap"
)

// HoldStockFund 持有指定股票的基金
type HoldStockFund struct {
	Fcode        string  `json:"FCODE"`
	Shortname    string  `json:"SHORTNAME"`
	Holdstock    string  `json:"HOLDSTOCK"`
	Stockname    string  `json:"STOCKNAME"`
	Zjzbl        float64 `json:"ZJZBL"`
	Tsrq         string  `json:"TSRQ"`
	Chgtype      string  `json:"CHGTYPE"`
	Chgnum       float64 `json:"CHGNUM"`
	SylY         float64 `json:"SYL_Y"`
	Syl6Y        float64 `json:"SYL_6Y"`
	Isbuy        string  `json:"ISBUY"`
	Stocktexch   string  `json:"STOCKTEXCH"`
	Newtexch     string  `json:"NEWTEXCH"`
	Zjzblchg     float64 `json:"ZJZBLCHG"`
	Zjzblchgtype string  `json:"ZJZBLCHGTYPE"`
}

// RespQueryFundByStock QueryFundByStock 原始api返回的结构
type RespQueryFundByStock struct {
	Datas struct {
		Datas      []HoldStockFund `json:"Datas"`
		Stocktexch string          `json:"STOCKTEXCH"`
		Newtexch   string          `json:"NEWTEXCH"`
	} `json:"Datas"`
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

// QueryFundByStock 根据股票查询基金
func (e EastMoney) QueryFundByStock(ctx context.Context, stockName, stockCode string) ([]HoldStockFund, error) {
	apiurl := fmt.Sprintf(
		"https://fundztapi.eastmoney.com/FundSpecialApiNew/FundSpecialApiGpGetFunds?pageIndex=1&pageSize=10000&isBuy=1&sortName=ZJZBL&sortType=DESC&deviceid=1&version=6.9.9&product=EFund&plat=Iphone&name=%s&code=%s",
		stockName,
		stockCode,
	)
	logging.Debug(ctx, "EastMoney QueryFundByStock "+apiurl+" begin")
	beginTime := time.Now()
	resp := RespQueryFundByStock{}
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFundByStock "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	return resp.Datas.Datas, nil
}
