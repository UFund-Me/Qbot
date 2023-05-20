// 获取机构评级统计

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

// RespOrgRating 统计评级接口返回结构
type RespOrgRating struct {
	Version string `json:"version"`
	Result  struct {
		Pages int         `json:"pages"`
		Data  []OrgRating `json:"data"`
		Count int         `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// OrgRating 机构评级统计
type OrgRating struct {
	// 时间段
	DateType string `json:"DATE_TYPE"`
	// 综合评级
	CompreRating string `json:"COMPRE_RATING"`
}

// OrgRatingList 评级列表
type OrgRatingList []OrgRating

// String 字符串输出
func (o OrgRatingList) String() string {
	s := []string{}
	for _, i := range o {
		s = append(s, fmt.Sprintf("%s:%s", i.DateType, i.CompreRating))
	}
	return strings.Join(s, "<br/>")
}

// QueryOrgRating 获取评级统计
func (e EastMoney) QueryOrgRating(ctx context.Context, secuCode string) (OrgRatingList, error) {
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/get"
	params := map[string]string{
		"source": "SECURITIES",
		"client": "APP",
		"type":   "RPT_RES_ORGRATING",
		"sty":    "DATE_TYPE,COMPRE_RATING",
		"filter": fmt.Sprintf(`(SECUCODE="%s")`, strings.ToUpper(secuCode)),
		"sr":     "1",
		"st":     "DATE_TYPE_CODE",
	}
	logging.Debug(ctx, "EastMoney QueryOrgRating "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespOrgRating{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(ctx, "EastMoney QueryOrgRating "+apiurl+" end",
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
