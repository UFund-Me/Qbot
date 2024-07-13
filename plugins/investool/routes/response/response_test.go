package response

import (
	"encoding/json"
	"errors"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/require"
)

func TestJSON(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	responseWriter := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(responseWriter)
	JSON(c, gin.H{"k": "v"})
	if c.Writer.Status() != 200 {
		t.Fatal("http status code error")
	}
	require.Equal(t, c.Writer.Status(), 200)

	j := responseWriter.Body.Bytes()
	r := Response{}
	err := json.Unmarshal(j, &r)
	require.Nil(t, err)
	require.Equal(t, r.Data.(map[string]interface{})["k"].(string), "v")
}

func TestErrJSON(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	responseWriter := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(responseWriter)
	ErrJSON(c, CodeInvalidParam)
	require.Equal(t, c.Writer.Status(), 200)
	j := responseWriter.Body.Bytes()
	r := Response{}
	err := json.Unmarshal(j, &r)
	require.Nil(t, err)
}

func TestRespond(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	responseWriter := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(responseWriter)
	Respond(c, 200, gin.H{"k": "v"}, CodeSuccess)
	require.Equal(t, c.Writer.Status(), 200)
	j := responseWriter.Body.Bytes()
	r := Response{}
	err := json.Unmarshal(j, &r)
	require.Nil(t, err)
	require.Equal(t, r.Data.(map[string]interface{})["k"].(string), "v")
}

func TestRespondWithExtraMsg(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	responseWriter := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(responseWriter)
	Respond(c, 200, gin.H{"k": "v"}, CodeSuccess, "xxx")
	require.Equal(t, c.Writer.Status(), 200)
	j := responseWriter.Body.Bytes()
	r := Response{}
	err := json.Unmarshal(j, &r)
	require.Nil(t, err)
	require.Equal(t, r.Data.(map[string]interface{})["k"].(string), "v")
	require.Equal(t, strings.Contains(r.Msg, "xxx"), true)
}

func TestRespondWithError(t *testing.T) {
	gin.SetMode(gin.ReleaseMode)
	responseWriter := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(responseWriter)
	Respond(c, 200, gin.H{"k": "v"}, errors.New("errxx"), "xxx")
	require.Equal(t, c.Writer.Status(), 200)
	j := responseWriter.Body.Bytes()
	r := Response{}
	err := json.Unmarshal(j, &r)
	require.Nil(t, err)
	require.Equal(t, r.Data.(map[string]interface{})["k"].(string), "v")
	require.Equal(t, strings.Contains(r.Msg, "errxx"), true)
}
