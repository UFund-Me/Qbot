package webserver

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestNewGinEngine(t *testing.T) {
	viper.SetDefault("server.mode", "release")
	defer viper.Reset()
	app := NewGinEngine(nil)
	assert.NotNil(t, app)
}

func TestGinBasicAuth(t *testing.T) {
	viper.Set("basic_auth.username", "axiaoxin")
	viper.Set("basic_auth.password", "axiaoxin")
	defer viper.Reset()
	gin.SetMode(gin.ReleaseMode)
	c, _ := gin.CreateTestContext(httptest.NewRecorder())
	c.Request, _ = http.NewRequest("GET", "/get", nil)
	auth := GinBasicAuth()
	auth(c)
	assert.Equal(t, c.Writer.Status(), http.StatusUnauthorized, "request without basic auth should return StatusUnauthorized")
}
