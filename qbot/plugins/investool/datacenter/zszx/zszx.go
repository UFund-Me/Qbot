// Package zszx 招商证券接口封装
// https://zszx.cmschina.com/
package zszx

import (
	"net/http"
	"time"
)

// Zszx 招商证券接口
type Zszx struct {
	// http 客户端
	HTTPClient *http.Client
}

// NewZszx 创建 Zszx 实例
func NewZszx() Zszx {
	hc := &http.Client{
		Timeout: time.Second * 60 * 5,
	}
	return Zszx{
		HTTPClient: hc,
	}
}
