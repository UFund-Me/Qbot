// 业务错误码定义

package response

import (
	"strings"

	"github.com/axiaoxin-com/goutils"
)

// 错误码中的 code 定义
const (
	failure = iota - 1
	success
	invalidParam
	notFound
	unknownError
)

// 错误码对象定义
var (
	CodeSuccess       = goutils.NewErrCode(success, "Success")
	CodeFailure       = goutils.NewErrCode(failure, "Failure")
	CodeInvalidParam  = goutils.NewErrCode(invalidParam, "Invalid Param")
	CodeNotFound      = goutils.NewErrCode(notFound, "Not Fount")
	CodeInternalError = goutils.NewErrCode(unknownError, "Unknown Error")
)

// IsInvalidParamError 判断错误信息中是否包含:参数错误
func IsInvalidParamError(err error) bool {
	return strings.Contains(err.Error(), "Invalid Param")
}
