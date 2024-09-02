package routes

import (
	"testing"

	"github.com/axiaoxin-com/goutils"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestPing(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	viper.Set("basic_auth.username", "admin")
	viper.Set("basic_auth.password", "admin")
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
