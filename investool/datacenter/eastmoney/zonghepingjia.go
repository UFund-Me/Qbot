// 获取智能诊股中的综合评价

package eastmoney

import (
	"context"
	"fmt"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"go.uber.org/zap"
)

// ZHPJ 综合评价
type ZHPJ struct {
	Securitycode  string      `json:"SecurityCode"`
	Updatetime    string      `json:"UpdateTime"`
	Totalscore    string      `json:"TotalScore"`
	Totalscorechg string      `json:"TotalScoreCHG"`
	Leadpre       interface{} `json:"LeadPre"`
	Risepro       interface{} `json:"RisePro"`
	// 消息面
	Msgcount string `json:"MsgCount"`
	// 主力资金
	Capitalscore string `json:"CapitalScore"`
	// 短期呈现
	D1 string `json:"D1"`
	// 公司质地
	Valuescore string `json:"ValueScore"`
	// 市场关注意愿
	Marketscorechg string `json:"MarketScoreCHG"`
	Status         string `json:"Status"`
	// 评分
	Pingfennum string `json:"PingFenNum"`
	// 打败 xxx 的股票
	Dabaishichangnum string `json:"DaBaiShiChangNum"`
	// 次日上涨概率
	Shangzhanggailvnum string `json:"ShangZhangGaiLvNum"`
	Checkzhengustatus  bool   `json:"CheckZhenGuStatus"`
}

// RespZongHePingJia 综合评价接口返回结构
type RespZongHePingJia struct {
	Result struct {
		Zonghepingjia ZHPJ `json:"ZongHePingJia"`
	} `json:"Result"`
	Status    int    `json:"Status"`
	Message   string `json:"Message"`
	Otherinfo struct {
	} `json:"OtherInfo"`
}

// QueryZongHePingJia 返回智能诊股中的综合评价
func (e EastMoney) QueryZongHePingJia(ctx context.Context, secuCode string) (ZHPJ, error) {
	fc := e.GetFC(secuCode)
	apiurl := "https://emstockdiag.eastmoney.com/api//ZhenGuShouYe/GetZongHePingJia"
	reqData := map[string]interface{}{
		"fc": fc,
	}
	logging.Debug(ctx, "EastMoney QueryZongHePingJia "+apiurl+" begin", zap.Any("reqData", reqData))
	beginTime := time.Now()
	req, err := goutils.NewHTTPJSONReq(ctx, apiurl, reqData)
	if err != nil {
		return ZHPJ{}, err
	}
	resp := RespZongHePingJia{}
	err = goutils.HTTPPOST(ctx, e.HTTPClient, req, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryZongHePingJia "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return ZHPJ{}, err
	}
	if resp.Status != 0 {
		return ZHPJ{}, fmt.Errorf("%s %#v", secuCode, resp.Message)
	}
	return resp.Result.Zonghepingjia, nil
}
