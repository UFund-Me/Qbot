package routes

import (
	"testing"

	"github.com/axiaoxin-com/goutils"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestRegisterRoutes(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	// Register 中的 basic auth 依赖 viper 配置
	viper.Set("basic_auth.username", "admin")
	viper.Set("basic_auth.password", "admin")
	viper.Set("env", "localhost")
	defer viper.Reset()

	Register(r)
	recorder, err := goutils.RequestHTTPHandler(
		r,
		"GET",
		"/x/ping",
		nil,
		map[string]string{"Authorization": "Basic YWRtaW46YWRtaW4="},
	)
	assert.Nil(t, err)
	assert.Equal(t, recorder.Code, 200)
}
