// 在这个文件中注册 URL handler

package routes

import "github.com/gin-gonic/gin"

// Routes 注册 API URL 路由
func Routes(app *gin.Engine) {
	app.GET("/", StockIndex)
	app.POST("/selector", StockSelector)
	app.POST("/checker", StockChecker)
	app.GET("/fund", FundIndex)
	app.GET("/fund/filter", FundFilter)
	app.POST("/fund/check", FundCheck)
	app.GET("/about", About)
	app.GET("/comment", Comment)
	app.GET("/fund/similarity", FundSimilarity)
	app.GET("/materials", Materials)
	app.POST("/fund/query_by_stock", QueryFundByStock)
	app.GET("/fund/managers", FundManagers)
}
