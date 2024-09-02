package chinabond

import (
	"context"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/corpix/uarand"
	"go.uber.org/zap"
)

// TreeItem 债券曲线树节点
type TreeItem struct {
	ID       string      `json:"id"`
	PID      string      `json:"pId"`
	Name     string      `json:"name"`
	IsParent string      `json:"isParent"`
	Open     string      `json:"open"`
	Checked  bool        `json:"checked"`
	Font     interface{} `json:"font"`
}

// RespQueryTree 债券曲线树 https://yield.chinabond.com.cn/cbweb-mn/yc/queryTree?locale=zh_CN 接口返回结果
type RespQueryTree []TreeItem

// QueryTree 查询债券曲线树数据，返回key为债券曲线名称，value为曲线名称对应的随机id
func (c ChinaBond) QueryTree(ctx context.Context) (map[string]string, error) {
	apiurl := "https://yield.chinabond.com.cn/cbweb-mn/yc/queryTree?locale=zh_CN"
	logging.Debug(ctx, "ChinaBond QueryTree "+apiurl+" begin")
	beginTime := time.Now()
	resp := RespQueryTree{}
	header := map[string]string{
		"User-Agent": uarand.GetRandom(),
	}
	err := goutils.HTTPGET(ctx, c.HTTPClient, apiurl, header, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"ChinaBond QueryTree "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	result := map[string]string{}
	for _, i := range resp {
		result[i.Name] = i.ID
	}
	return result, nil
}
