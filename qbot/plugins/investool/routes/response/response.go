// Package response 提供统一的 JSON 返回结构，可以通过配置设置具体返回的 code 字段为 int 或者 string
package response

import (
	"fmt"
	"net/http"

	"github.com/axiaoxin-com/goutils"
	"github.com/gin-gonic/gin"
)

// Response 统一的返回结构定义
type Response struct {
	Code interface{} `json:"code"`
	Msg  string      `json:"msg"`
	Data interface{} `json:"data"`
}

// JSON 返回 HTTP 状态码为 200 的统一成功结构
func JSON(c *gin.Context, data interface{}) {
	Respond(c, http.StatusOK, data, CodeSuccess)
}

// ErrJSON 返回 HTTP 状态码为 200 的统一失败结构
func ErrJSON(c *gin.Context, err error, extraMsgs ...interface{}) {
	Respond(c, http.StatusOK, nil, err, extraMsgs...)
}

// Respond encapsulates c.JSON
// debug mode respond indented json
func Respond(c *gin.Context, status int, data interface{}, errcode error, extraMsgs ...interface{}) {
	// 初始化 code 、 msg 为失败
	code, msg, _ := CodeFailure.Decode()

	if ec, ok := errcode.(*goutils.ErrCode); ok {
		// 如果是返回码，正常处理
		code, msg, _ = ec.Decode()
		// 存在 errs 则将 errs 信息添加的 msg
		if len(ec.Errs()) > 0 {
			msg = fmt.Sprint(msg, " ", ec.Error())
		}
	} else {
		// 支持 errcode 参数直接传 error ，如果是 error ，则将 error 信息添加到 msg
		msg = fmt.Sprint(msg, " ", errcode.Error())
	}

	// 将 extraMsgs 添加到 msg
	if len(extraMsgs) > 0 {
		msg = fmt.Sprint(msg, "; ", extraMsgs)
	}

	resp := Response{
		Code: code,
		Msg:  msg,
		Data: data,
	}
	c.Header("x-response-code", fmt.Sprint(code))
	if gin.Mode() == gin.ReleaseMode {
		c.JSON(status, resp)
	} else {
		c.IndentedJSON(status, resp)
	}
}
