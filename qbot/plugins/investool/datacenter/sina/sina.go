// Package sina 新浪财经接口封装
package sina

import (
	"net/http"
	"time"
)

// Sina 新浪财经数据源
type Sina struct {
	// http 客户端
	HTTPClient *http.Client
}

// NewSina 创建 Sina 实例
func NewSina() Sina {
	hc := &http.Client{
		Timeout: time.Second * 60 * 5,
	}
	return Sina{
		HTTPClient: hc,
	}
}
