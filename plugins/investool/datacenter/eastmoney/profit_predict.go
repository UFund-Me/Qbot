// 获取盈利预测

package eastmoney

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"go.uber.org/zap"
)

// RespProfitPredict 盈利预测接口返回结构
type RespProfitPredict struct {
	Version string `json:"version"`
	Result  struct {
		Pages int             `json:"pages"`
		Data  []ProfitPredict `json:"data"`
		Count int             `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// ProfitPredict 盈利预测
type ProfitPredict struct {
	// 年份
	PredictYear int `json:"PREDICT_YEAR"`
	// 预测每股收益
	Eps float64 `json:"EPS"`
	// 预测市盈率
	Pe float64 `json:"PE"`
}

// ProfitPredictList 预测列表
type ProfitPredictList []ProfitPredict

func (p ProfitPredictList) String() string {
	s := []string{}
	for _, i := range p {
		s = append(s, fmt.Sprintf("%d | 预测每股收益:%f 预测市盈率:%f", i.PredictYear, i.Eps, i.Pe))
	}
	return strings.Join(s, "<br/>")
}

// QueryProfitPredict 获取盈利预测
func (e EastMoney) QueryProfitPredict(ctx context.Context, secuCode string) (ProfitPredictList, error) {
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/get"
	params := map[string]string{
		"source": "SECURITIES",
		"client": "APP",
		"type":   "RPT_RES_PROFITPREDICT",
		"sty":    "PREDICT_YEAR,EPS,PE",
		"filter": fmt.Sprintf(`(SECUCODE="%s")`, strings.ToUpper(secuCode)),
		"sr":     "1",
		"st":     "PREDICT_YEAR",
	}
	logging.Debug(ctx, "EastMoney QueryProfitPredict "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespProfitPredict{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(ctx, "EastMoney QueryProfitPredict "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", secuCode, resp)
	}
	return resp.Result.Data, nil
}
