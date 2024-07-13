// Package chinabond 接口封装
// https://yield.chinabond.com.cn/cbweb-mn/yield_main?locale=zh_CN
package chinabond

import (
	"net/http"
	"time"
)

// ChinaBond 中国债券信息网
type ChinaBond struct {
	// http 客户端
	HTTPClient *http.Client
}

// NewChinaBond 创建 ChinaBond 实例
func NewChinaBond() ChinaBond {
	hc := &http.Client{
		Timeout: time.Second * 60 * 5,
	}
	return ChinaBond{
		HTTPClient: hc,
	}
}
