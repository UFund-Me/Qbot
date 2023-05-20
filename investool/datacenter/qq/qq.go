// Package qq 腾讯证券接口封装
package qq

import (
	"net/http"
	"time"
)

// QQ 新浪财经数据源
type QQ struct {
	// http 客户端
	HTTPClient *http.Client
}

// NewQQ 创建 QQ 实例
func NewQQ() QQ {
	hc := &http.Client{
		Timeout: time.Second * 60 * 5,
	}
	return QQ{
		HTTPClient: hc,
	}
}
