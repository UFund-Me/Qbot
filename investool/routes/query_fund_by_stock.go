// 根据股票查基金

package routes

import (
	"net/http"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/investool/version"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

// ParamQueryFundByStock QueryFundByStock 请求参数
type ParamQueryFundByStock struct {
	Keywords string `form:"keywords" binding:"required"`
}

// QueryFundByStock 股票选基
func QueryFundByStock(c *gin.Context) {
	data := gin.H{
		"Env":       viper.GetString("env"),
		"Version":   version.Version,
		"PageTitle": "InvesTool | 基金 | 股票选基",
		"Error":     "",
	}

	param := ParamQueryFundByStock{}
	if err := c.ShouldBind(&param); err != nil {
		data["Error"] = err.Error()
		c.JSON(http.StatusOK, data)
		return
	}
	keywords := goutils.SplitStringFields(param.Keywords)
	searcher := core.NewSearcher(c)
	dlist, err := searcher.SearchFundByStock(c, keywords...)
	if err != nil {
		data["Error"] = err.Error()
		c.JSON(http.StatusOK, data)
		return
	}
	data["Funds"] = dlist
	c.HTML(http.StatusOK, "hold_stock_fund.html", data)
	return
}
