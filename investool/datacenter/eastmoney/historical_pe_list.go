// 获取历史市盈率

package eastmoney

import (
	"context"
	"errors"
	"strconv"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"go.uber.org/zap"
)

// RespHistoricalPE 历史市盈率接口返回结构
type RespHistoricalPE struct {
	Data [][]struct {
		Securitycode string `json:"SECURITYCODE"`
		Datetype     string `json:"DATETYPE"`
		Sl           string `json:"SL"`
		Endate       string `json:"ENDATE"`
		Value        string `json:"VALUE"`
	} `json:"data"`
	Pe [][]struct {
		Securitycode string `json:"SECURITYCODE"`
		Pe30         string `json:"PE30"`
		Pe50         string `json:"PE50"`
		Pe70         string `json:"PE70"`
		Total        string `json:"TOTAL"`
		Rn1          string `json:"RN1"`
		Rn2          string `json:"RN2"`
		Rn3          string `json:"RN3"`
	} `json:"pe"`
}

// HistoricalPE 历史 pe
type HistoricalPE struct {
	Value float64
	Date  string
}

// HistoricalPEList 历史 pe 列表
type HistoricalPEList []HistoricalPE

// GetMidValue 获取历史 pe 中位数
func (h HistoricalPEList) GetMidValue(ctx context.Context) (float64, error) {
	values := []float64{}
	for _, i := range h {
		values = append(values, i.Value)
	}
	return goutils.MidValueFloat64(values)
}

// QueryHistoricalPEList 获取历史市盈率
func (e EastMoney) QueryHistoricalPEList(ctx context.Context, secuCode string) (HistoricalPEList, error) {
	apiurl := "https://emfront.eastmoney.com/APP_HSF10/CPBD/GZFX"
	params := map[string]string{
		"code": e.GetFC(secuCode),
		"year": "4", // 10 年
		"type": "1", // 市盈率
	}
	logging.Debug(ctx, "EastMoney QueryHistoricalPEList "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespHistoricalPE{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryHistoricalPEList "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	result := HistoricalPEList{}
	if len(resp.Data) == 0 {
		return nil, errors.New("no historical pe data")
	}
	for _, i := range resp.Data[0] {
		value, err := strconv.ParseFloat(i.Value, 64)
		if err != nil {
			logging.Error(ctx, "QueryHistoricalPEList ParseFloat error:"+err.Error())
			continue
		}
		pe := HistoricalPE{
			Date:  i.Endate,
			Value: value,
		}
		result = append(result, pe)
	}
	return result, nil
}
