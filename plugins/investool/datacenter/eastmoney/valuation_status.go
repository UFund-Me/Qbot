// 获取估值状态

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

// RespValuation 估值状态接口返回结构
type RespValuation struct {
	Version string `json:"version"`
	Result  struct {
		Pages int `json:"pages"`
		Data  []struct {
			ValationStatus string `json:"VALATION_STATUS"`
		} `json:"data"`
		Count int `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// QueryValuationStatus 获取估值状态
func (e EastMoney) QueryValuationStatus(ctx context.Context, secuCode string) (map[string]string, error) {
	valuations := map[string]string{}
	secuCode = strings.ToUpper(secuCode)
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/get"
	// 市盈率估值
	params := map[string]string{
		"type":   "RPT_VALUATIONSTATUS",
		"sty":    "VALATION_STATUS",
		"p":      "1",
		"ps":     "1",
		"var":    "source=DataCenter",
		"client": "APP",
		"filter": fmt.Sprintf(`(SECUCODE="%s")(INDICATOR_TYPE="1")`, secuCode),
	}
	beginTime := time.Now()
	apiurl1, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	logging.Debug(ctx, "EastMoney QueryValuationStatus "+apiurl1+" begin", zap.Any("params", params))
	if err != nil {
		return nil, err
	}
	resp := RespValuation{}
	if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl1, nil, &resp); err != nil {
		return nil, err
	}
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryValuationStatus "+apiurl1+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", secuCode, resp)
	}
	if len(resp.Result.Data) > 0 {
		valuations["市盈率"] = resp.Result.Data[0].ValationStatus
	}

	// 市净率估值
	params["filter"] = fmt.Sprintf(`(SECUCODE="%s")(INDICATOR_TYPE="2")`, secuCode)
	beginTime = time.Now()
	apiurl2, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	logging.Debug(ctx, "EastMoney QueryValuationStatus "+apiurl2+" begin", zap.Any("params", params))
	if err != nil {
		return nil, err
	}
	if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl2, nil, &resp); err != nil {
		return nil, err
	}
	latency = time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryValuationStatus "+apiurl2+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", secuCode, resp)
	}
	if len(resp.Result.Data) > 0 {
		valuations["市净率"] = resp.Result.Data[0].ValationStatus
	}

	// 市销率估值
	params["filter"] = fmt.Sprintf(`(SECUCODE="%s")(INDICATOR_TYPE="3")`, secuCode)
	beginTime = time.Now()
	apiurl3, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	logging.Debug(ctx, "EastMoney QueryValuationStatus "+apiurl3+" begin", zap.Any("params", params))
	if err != nil {
		return nil, err
	}
	if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl3, nil, &resp); err != nil {
		return nil, err
	}
	latency = time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryValuationStatus "+apiurl3+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", secuCode, resp)
	}
	if len(resp.Result.Data) > 0 {
		valuations["市销率"] = resp.Result.Data[0].ValationStatus
	}

	// 市现率估值
	params["filter"] = fmt.Sprintf(`(SECUCODE="%s")(INDICATOR_TYPE="4")`, secuCode)
	beginTime = time.Now()
	apiurl4, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	logging.Debug(ctx, "EastMoney QueryValuationStatus "+apiurl4+" begin", zap.Any("params", params))
	if err != nil {
		return nil, err
	}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl4, nil, &resp)
	latency = time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryValuationStatus "+apiurl4+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", secuCode, resp)
	}
	if len(resp.Result.Data) > 0 {
		valuations["市现率"] = resp.Result.Data[0].ValationStatus
	}

	return valuations, nil
}
