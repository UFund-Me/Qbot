// 获取智能诊股中的价值评估

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

// JZPG 价值评估
type JZPG struct {
	// 股票名
	Secname string `json:"SecName"`
	// 行业名
	Industryname string `json:"IndustryName"`
	Type         string `json:"Type"`
	// 当前排名
	Valueranking string `json:"ValueRanking"`
	// 排名总数
	Total string `json:"Total"`
	// 整体质地
	Valuetotalscore string `json:"ValueTotalScore"`
	Reportdate      string `json:"ReportDate"`
	Reporttype      string `json:"ReportType"`
	// 盈利能力
	Profitabilityscore string `json:"ProfitabilityScore"`
	// 成长能力
	Growupscore string `json:"GrowUpScore"`
	// 营运偿债能力
	Operationscore string `json:"OperationScore"`
	// 现金流
	Cashflowscore string `json:"CashFlowScore"`
	// 估值
	Valuationscore string `json:"ValuationScore"`
}

// GetValueRanking 当前排名
func (j JZPG) GetValueRanking() string {
	return strings.Split(j.Valueranking, "|")[0]
}

// GetProfitabilityScore 盈利能力
func (j JZPG) GetProfitabilityScore() string {
	return strings.Split(j.Profitabilityscore, "|")[0]
}

// GetGrowUpScore 成长能力
func (j JZPG) GetGrowUpScore() string {
	return strings.Split(j.Growupscore, "|")[0]
}

// GetOperationScore 营运偿债能力
func (j JZPG) GetOperationScore() string {
	return strings.Split(j.Operationscore, "|")[0]
}

// GetCashFlowScore 现金流能力
func (j JZPG) GetCashFlowScore() string {
	return strings.Split(j.Cashflowscore, "|")[0]
}

// GetValuationScore 估值能力
func (j JZPG) GetValuationScore() string {
	return strings.Split(j.Valuationscore, "|")[0]
}

// GetValueTotalScore 整体质地
func (j JZPG) GetValueTotalScore() string {
	return strings.Split(j.Valuetotalscore, "|")[0]
}

func (j JZPG) String() string {
	return fmt.Sprintf(
		"%s属于%s行业，排名%s/%s。\n盈利能力%s，成长能力%s，营运偿债能力%s，现金流%s，估值%s，整体质地%s。",
		j.Secname,
		j.Industryname,
		j.GetValueRanking(),
		j.Total,
		j.GetProfitabilityScore(),
		j.GetGrowUpScore(),
		j.GetOperationScore(),
		j.GetCashFlowScore(),
		j.GetValuationScore(),
		j.GetValueTotalScore(),
	)
}

// RespJiaZhiPingGu 综合评价接口返回结构
type RespJiaZhiPingGu struct {
	Result struct {
		JiazhipingguGaiyao      JZPG `json:"JiaZhiPingGu_GaiYao"`
		JiazhipingguWuweitulist []struct {
			Reportdate         string `json:"ReportDate"`
			Reporttype         string `json:"ReportType"`
			Profitabilityscore string `json:"ProfitabilityScore"`
			Growupscore        string `json:"GrowUpScore"`
			Operationscore     string `json:"OperationScore"`
			Cashflowscore      string `json:"CashFlowScore"`
			Valuationscore     string `json:"ValuationScore"`
		} `json:"JiaZhiPingGu_WuWeiTuList"`
	} `json:"Result"`
	Status    int    `json:"Status"`
	Message   string `json:"Message"`
	Otherinfo struct {
	} `json:"OtherInfo"`
}

// QueryJiaZhiPingGu 返回智能诊股中的价值评估
func (e EastMoney) QueryJiaZhiPingGu(ctx context.Context, secuCode string) (JZPG, error) {
	fc := e.GetFC(secuCode)
	apiurl := "https://emstockdiag.eastmoney.com/api/ZhenGuShouYe/GetJiaZhiPingGu"
	reqData := map[string]interface{}{
		"fc": fc,
	}
	logging.Debug(ctx, "EastMoney QueryJiaZhiPingGu "+apiurl+" begin", zap.Any("reqData", reqData))
	beginTime := time.Now()
	req, err := goutils.NewHTTPJSONReq(ctx, apiurl, reqData)
	if err != nil {
		return JZPG{}, err
	}
	resp := RespJiaZhiPingGu{}
	err = goutils.HTTPPOST(ctx, e.HTTPClient, req, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryJiaZhiPingGu "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return JZPG{}, err
	}
	if resp.Status != 0 {
		return JZPG{}, fmt.Errorf("%s %#v", secuCode, resp.Message)
	}
	return resp.Result.JiazhipingguGaiyao, nil
}
