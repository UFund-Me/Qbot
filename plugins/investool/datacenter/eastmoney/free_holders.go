// 获取十大流通股东

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

// FreeHolder 流通股东
type FreeHolder struct {
	// 日期
	EndDate string `json:"END_DATE"`
	// 股东名称
	HolderName string `json:"HOLDER_NAME"`
	// 股东代码
	HolderCode string `json:"HOLDER_CODE"`
	// 持股数
	HoldNum int `json:"HOLD_NUM"`
	// 占流通股比
	FreeHoldnumRatio float64 `json:"FREE_HOLDNUM_RATIO"`
	// 环比增减
	FreeRatioQoq string `json:"FREE_RATIO_QOQ"`
	// 1:机构 0:个人
	IsHoldorg string `json:"IS_HOLDORG"`
	// 持股数排名
	HolderRank int `json:"HOLDER_RANK"`
}

// FreeHolderList ...
type FreeHolderList []FreeHolder

func (f FreeHolderList) String() string {
	s := []string{}
	for i, h := range f {
		fs := fmt.Sprintf("%d.%s|%.2f%%|%v", i+1, h.HolderName, h.FreeHoldnumRatio, h.FreeRatioQoq)
		s = append(s, fs)
	}
	return strings.Join(s, "<br/>")
}

// RespFreeHolders QueryFreeHolders 返回json结构
type RespFreeHolders struct {
	Version string `json:"version"`
	Result  struct {
		Pages int            `json:"pages"`
		Data  FreeHolderList `json:"data"`
		Count int            `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// QueryFreeHolders 获取前十大流通股东信息
func (e EastMoney) QueryFreeHolders(ctx context.Context, secuCode string) (FreeHolderList, error) {
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/v1/get"
	params := map[string]string{
		"reportName": "RPT_F10_EH_FREEHOLDERS",
		"columns":    "END_DATE,HOLDER_NAME,HOLDER_CODE,HOLD_NUM,FREE_HOLDNUM_RATIO,FREE_RATIO_QOQ,IS_HOLDORG,HOLDER_RANK",
		"filter":     fmt.Sprintf(`(SECUCODE="%s")`, strings.ToUpper(secuCode)),
		"pageSize":   "10",
	}
	logging.Debug(ctx, "EastMoney QueryFreeHolders "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespFreeHolders{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFreeHolders "+apiurl+" end",
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
