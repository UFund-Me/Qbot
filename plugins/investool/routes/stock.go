// 首页

package routes

import (
	"fmt"
	"math"
	"net/http"
	"strings"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/investool/version"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

// StockIndex 股票页面
func StockIndex(c *gin.Context) {
	data := gin.H{
		"Env":          viper.GetString("env"),
		"Version":      version.Version,
		"PageTitle":    "InvesTool | 股票",
		"Error":        "",
		"IndustryList": models.StockIndustryList,
	}
	c.HTML(http.StatusOK, "stock_index.html", data)
	return
}

// ParamStockSelector StockSelector 请求参数
type ParamStockSelector struct {
	Filter            eastmoney.Filter
	CheckerOptions    core.CheckerOptions
	FilterWithChecker bool `form:"selector_with_checker"`
}

// StockSelector 返回基本面筛选结果json
func StockSelector(c *gin.Context) {
	data := gin.H{
		"Env":       viper.GetString("env"),
		"Version":   version.Version,
		"PageTitle": "InvesTool | 股票 | 基本面筛选",
		"Error":     "",
		"Stocks":    models.StockList{},
	}

	param := ParamStockSelector{}
	if err := c.ShouldBind(&param); err != nil {
		data["Error"] = err.Error()
		c.JSON(http.StatusOK, data)
		return
	}
	var checker *core.Checker
	if param.FilterWithChecker {
		checker = core.NewChecker(c, param.CheckerOptions)
	}

	selector := core.NewSelector(c, param.Filter, checker)
	stocks, err := selector.AutoFilterStocks(c)
	if err != nil {
		data["Error"] = err.Error()
		c.JSON(http.StatusOK, data)
		return
	}
	stocks.SortByPriceSpace()
	dlist := models.ExportorDataList{}
	for _, s := range stocks {
		dlist = append(dlist, models.NewExportorData(c, s))
	}
	data["Stocks"] = dlist
	c.JSON(http.StatusOK, data)
	return
}

// ParamStockChecker StockChecker 请求参数
type ParamStockChecker struct {
	Keyword        string `form:"checker_keyword"`
	CheckerOptions core.CheckerOptions
}

// StockChecker 处理个股检测
func StockChecker(c *gin.Context) {
	data := gin.H{
		"Env":       viper.GetString("env"),
		"Version":   version.Version,
		"PageTitle": "InvesTool | 股票 | 个股检测",
		"Error":     "",
	}
	param := ParamStockChecker{}
	if err := c.ShouldBind(&param); err != nil {
		data["Error"] = err.Error()
		c.JSON(http.StatusOK, data)
		return
	}
	if param.Keyword == "" {
		data["Error"] = "请填写股票代码或简称"
		c.JSON(http.StatusOK, data)
		return
	}
	searcher := core.NewSearcher(c)
	keywords := goutils.SplitStringFields(param.Keyword)
	if len(keywords) > 50 {
		data["Error"] = "股票数量超过限制"
		c.JSON(http.StatusOK, data)
		return
	}
	stocks, err := searcher.SearchStocks(c, keywords)
	if err != nil {
		data["Error"] = err.Error()
		c.JSON(http.StatusOK, data)
		return
	}
	checker := core.NewChecker(c, param.CheckerOptions)
	results := []core.CheckResult{}
	stockNames := []string{}
	finaReportNames := []string{}
	finaAppointPublishDates := []string{}
	lines := []gin.H{}
	mainInflows := []string{}

	for _, stock := range stocks {
		result, _ := checker.CheckFundamentals(c, stock)
		results = append(results, result)
		stockName := fmt.Sprintf("%s-%s", stock.BaseInfo.SecurityNameAbbr, stock.BaseInfo.Secucode)
		stockNames = append(stockNames, stockName)
		mainInflows = append(mainInflows, stock.MainMoneyNetInflows.String())

		finaReportName := ""
		if len(stock.HistoricalFinaMainData) > 0 {
			finaReportName = stock.HistoricalFinaMainData[0].ReportDateName
		}
		finaReportNames = append(finaReportNames, finaReportName)

		finaAppointPublishDates = append(finaAppointPublishDates, strings.Split(stock.FinaAppointPublishDate, " ")[0])

		roeList := goutils.ReversedFloat64Slice(
			stock.HistoricalFinaMainData.ValueList(
				c,
				eastmoney.ValueListTypeROE,
				param.CheckerOptions.CheckYears,
				eastmoney.FinaReportTypeYear,
			))
		yearLabels := []string{}
		year := time.Now().Year()
		yearcount := int(math.Min(float64(param.CheckerOptions.CheckYears), float64(len(roeList))))
		for i := yearcount; i > 0; i-- {
			yearLabels = append(yearLabels, fmt.Sprint(year-i))
		}
		revenueList := []float64{}
		for _, r := range goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
			c,
			eastmoney.ValueListTypeRevenue,
			param.CheckerOptions.CheckYears,
			eastmoney.FinaReportTypeYear,
		)) {
			revenueList = append(revenueList, r/100000000.0) // 亿
		}
		grossProfitList := []float64{}
		for _, p := range goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
			c,
			eastmoney.ValueListTypeGrossProfit,
			param.CheckerOptions.CheckYears,
			eastmoney.FinaReportTypeYear,
		)) {
			grossProfitList = append(grossProfitList, p/100000000.0)
		}
		netProfitList := []float64{}
		for _, p := range goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
			c,
			eastmoney.ValueListTypeNetProfit,
			param.CheckerOptions.CheckYears,
			eastmoney.FinaReportTypeYear,
		)) {
			netProfitList = append(netProfitList, p/100000000.0)
		}

		line := gin.H{
			"legends": []string{"ROE", "EPS", "ROA", "毛利率", "净利率", "营收", "毛利润", "净利润"},
			"xAxis":   yearLabels,
			"data": [][]float64{
				roeList,
				goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
					c,
					eastmoney.ValueListTypeEPS,
					param.CheckerOptions.CheckYears,
					eastmoney.FinaReportTypeYear,
				)),
				goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
					c,
					eastmoney.ValueListTypeROA,
					param.CheckerOptions.CheckYears,
					eastmoney.FinaReportTypeYear,
				)),
				goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
					c,
					eastmoney.ValueListTypeMLL,
					param.CheckerOptions.CheckYears,
					eastmoney.FinaReportTypeYear,
				)),
				goutils.ReversedFloat64Slice(stock.HistoricalFinaMainData.ValueList(
					c,
					eastmoney.ValueListTypeJLL,
					param.CheckerOptions.CheckYears,
					eastmoney.FinaReportTypeYear,
				)),
				revenueList,
				grossProfitList,
				netProfitList,
			},
		}
		lines = append(lines, line)
	}
	data["Results"] = results
	data["StockNames"] = stockNames
	data["FinaReportNames"] = finaReportNames
	data["FinaAppointPublishDates"] = finaAppointPublishDates
	data["Lines"] = lines
	data["MainMoneyNetInflows"] = mainInflows
	c.JSON(http.StatusOK, data)
	return
}
