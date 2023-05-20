// 关键词搜索

package qq

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"go.uber.org/zap"
)

// SearchResult 搜索结果
type SearchResult struct {
	// 数字代码
	SecurityCode string
	// 带后缀的代码
	Secucode string
	// 股票名称
	Name string
}

// KeywordSearch 关键词搜索， 股票、代码、拼音
func (q QQ) KeywordSearch(ctx context.Context, kw string) (results []SearchResult, err error) {
	apiurl := fmt.Sprintf("https://smartbox.gtimg.cn/s3/?v=2&q=%s&t=all&c=1", kw)
	logging.Debug(ctx, "QQ KeywordSearch "+apiurl+" begin")
	beginTime := time.Now()
	resp, err := goutils.HTTPGETRaw(ctx, q.HTTPClient, apiurl, nil)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(ctx, "QQ KeywordSearch "+apiurl+" end", zap.Int64("latency(ms)", latency), zap.Any("resp", string(resp)))
	if err != nil {
		return nil, err
	}
	respMap := map[string]string{}
	for _, line := range strings.Split(string(resp), ";") {
		lineitems := strings.Split(line, "=")
		if len(lineitems) != 2 {
			continue
		}
		k := strings.TrimSpace(lineitems[0])
		v := strings.TrimSpace(lineitems[1])
		respMap[k] = strings.Trim(v, `"`)
	}
	logging.Debugf(ctx, "respMap: %#v", respMap)
	resultsStrs := strings.Split(respMap["v_hint"], "^")
	logging.Debugs(ctx, "resultsStrs:", resultsStrs)
	for _, rs := range resultsStrs {
		matchedSlice := strings.Split(rs, "~")
		if len(matchedSlice) < 3 {
			logging.Debugf(ctx, "invalid matchedSlice:%v", matchedSlice)
			continue
		}
		market, securityCode, name := matchedSlice[0], matchedSlice[1], matchedSlice[2]
		// unicode -> cn
		name, err = strconv.Unquote(strings.Replace(strconv.Quote(string(name)), `\\u`, `\u`, -1))
		if err != nil {
			return nil, err
		}
		result := SearchResult{
			Secucode:     securityCode + "." + market,
			SecurityCode: securityCode,
			Name:         name,
		}
		results = append(results, result)
	}
	return
}
