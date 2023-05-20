// 基金

package routes

import (
	"net/http"
	"sync"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/investool/version"
	"github.com/axiaoxin-com/logging"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

// ParamFundIndex FundIndex 请求参数
type ParamFundIndex struct {
	PageNum  int    `json:"page_num"  form:"page_num"`
	PageSize int    `json:"page_size" form:"page_size"`
	Sort     int    `json:"sort"      form:"sort"`
	Type     string `json:"type"      form:"type"`
}

// FundIndex godoc
func FundIndex(c *gin.Context) {
	fundList := models.Fund4433List
	p := ParamFundIndex{
		PageNum:  1,
		PageSize: 10,
		Sort:     models.FundSortTypeWeek,
	}
	if err := c.ShouldBind(&p); err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金",
			"Error":     err.Error(),
		}
		c.HTML(http.StatusOK, "fund_index.html", data)
		return
	}

	// 过滤
	if p.Type != "" {
		fundList = fundList.FilterByType(p.Type)
	}
	// 排序
	if p.Sort > 0 {
		fundList.Sort(models.FundSortType(p.Sort))
	}
	// 分页
	totalCount := len(fundList)
	pagi := goutils.PaginateByPageNumSize(totalCount, p.PageNum, p.PageSize)
	result := fundList[pagi.StartIndex:pagi.EndIndex]
	data := gin.H{
		"Env":           viper.GetString("env"),
		"Version":       version.Version,
		"PageTitle":     "InvesTool | 基金",
		"URLPath":       "/fund",
		"FundList":      result,
		"Pagination":    pagi,
		"IndexParam":    p,
		"UpdatedAt":     models.SyncFundTime.Format("2006-01-02 15:04:05"),
		"AllFundCount":  len(models.FundAllList),
		"Fund4433Count": totalCount,
		"FundTypes":     models.Fund4433TypeList,
	}
	c.HTML(http.StatusOK, "fund_index.html", data)
	return
}

// ParamFundFilter FundFilter 请求参数
type ParamFundFilter struct {
	ParamFundListFilter models.ParamFundListFilter
	ParamFundIndex      ParamFundIndex
}

// FundFilter godoc
func FundFilter(c *gin.Context) {
	p := ParamFundFilter{
		ParamFundListFilter: models.ParamFundListFilter{
			MinScale:             2.0,
			MaxScale:             50.0,
			MinEstabYears:        5.0,
			MinManagerYears:      5.0,
			Year1RankRatio:       25.0,
			ThisYear235RankRatio: 25.0,
			Month6RankRatio:      33.33,
			Month3RankRatio:      33.33,
		},
		ParamFundIndex: ParamFundIndex{
			PageNum:  1,
			PageSize: 10,
			Sort:     0,
		},
	}
	if err := c.ShouldBind(&p); err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金严选",
			"Error":     err.Error(),
		}
		c.HTML(http.StatusOK, "fund_filter.html", data)
		return
	}
	fundList := models.FundAllList.Filter(c, p.ParamFundListFilter)
	fundTypes := fundList.Types()
	// 过滤
	if p.ParamFundIndex.Type != "" {
		fundList = fundList.FilterByType(p.ParamFundIndex.Type)
	}
	// 排序
	if p.ParamFundIndex.Sort > 0 {
		fundList.Sort(models.FundSortType(p.ParamFundIndex.Sort))
	}
	// 分页
	pagi := goutils.PaginateByPageNumSize(len(fundList), p.ParamFundIndex.PageNum, p.ParamFundIndex.PageSize)
	result := fundList[pagi.StartIndex:pagi.EndIndex]
	data := gin.H{
		"Env":         viper.GetString("env"),
		"Version":     version.Version,
		"PageTitle":   "InvesTool | 基金 | 基金严选",
		"URLPath":     "/fund/filter",
		"FundList":    result,
		"Pagination":  pagi,
		"IndexParam":  p.ParamFundIndex,
		"FilterParam": p.ParamFundListFilter,
		"FundTypes":   fundTypes,
	}
	c.HTML(http.StatusOK, "fund_filter.html", data)
	return
}

// ParamFundCheck FundCheck 请求参数
type ParamFundCheck struct {
	// 基金代码
	Code string `json:"fundcode"                 form:"fundcode"`
	// 基金规模最小值（亿）
	MinScale float64 `json:"min_scale"                form:"min_scale"`
	// 基金规模最大值（亿）
	MaxScale float64 `json:"max_scale"                form:"max_scale"`
	// 基金经理管理该基金最低年限
	MinManagerYears float64 `json:"min_manager_years"        form:"min_manager_years"`
	// 最近一年收益率排名比
	Year1RankRatio float64 `json:"year_1_rank_ratio"        form:"year_1_rank_ratio"`
	// 今年来、最近两年、最近三年、最近五年收益率排名比
	ThisYear235RankRatio float64 `json:"this_year_235_rank_ratio" form:"this_year_235_rank_ratio"`
	// 最近六月收益率排名比
	Month6RankRatio float64 `json:"month_6_rank_ratio"       form:"month_6_rank_ratio"`
	// 最近三月收益率排名比
	Month3RankRatio float64 `json:"month_3_rank_ratio"       form:"month_3_rank_ratio"`
	// 1,3,5年波动率平均值的最大值
	Max135AvgStddev float64 `json:"max_135_avg_stddev"       form:"max_135_avg_stddev"`
	// 1,3,5年夏普比率平均值的最小值
	Min135AvgSharp float64 `json:"min_135_avg_sharp"        form:"min_135_avg_sharp"`
	// 1,3,5年最大回撤率平均值的最大值
	Max135AvgRetr float64 `json:"max_135_avg_retr"         form:"max_135_avg_retr"`
	// 是否检测持仓个股
	CheckStocks bool `json:"check_stocks"             form:"check_stocks"`
	// 股票检测参数
	StockCheckerOptions core.CheckerOptions
}

// FundCheck godoc
func FundCheck(c *gin.Context) {
	p := ParamFundCheck{
		MinScale:             2.0,
		MaxScale:             50.0,
		MinManagerYears:      5.0,
		Year1RankRatio:       25.0,
		ThisYear235RankRatio: 25.0,
		Month6RankRatio:      33.33,
		Month3RankRatio:      33.33,
		Max135AvgStddev:      25.0,
		Min135AvgSharp:       1.0,
		Max135AvgRetr:        25.0,
		CheckStocks:          false,
	}
	if err := c.ShouldBind(&p); err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金检测",
			"Error":     err.Error(),
		}
		c.JSON(http.StatusOK, data)
		return
	}

	if p.Code == "" {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金检测",
			"Error":     "请填写基金代码",
		}
		c.JSON(http.StatusOK, data)
		return
	}

	codes := goutils.SplitStringFields(p.Code)
	searcher := core.NewSearcher(c)
	funds, err := searcher.SearchFunds(c, codes)
	if err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金检测",
			"Error":     err.Error(),
		}
		c.JSON(http.StatusOK, data)
		return
	}

	if !p.CheckStocks {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金检测",
			"Funds":     funds,
			"Param":     p,
		}
		c.JSON(http.StatusOK, data)
		return
	}

	if len(funds) > 50 {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金检测",
			"Error":     "基金数量超过限制",
			"Funds":     funds,
			"Param":     p,
		}
		c.JSON(http.StatusOK, data)
		return
	}
	stockCheckResults := map[string]core.FundStocksCheckResult{}
	checker := core.NewChecker(c, p.StockCheckerOptions)
	var wg sync.WaitGroup
	var mu sync.Mutex
	for _, fund := range funds {
		wg.Add(1)
		go func(fund *models.Fund) {
			defer func() {
				wg.Done()
			}()
			checkResult, err := checker.CheckFundStocks(c, fund)
			if err != nil {
				logging.Errorf(c, "CheckFundStocks code:%s err:%v", fund.Code, err)
				return
			}
			mu.Lock()
			stockCheckResults[fund.Code] = checkResult
			mu.Unlock()
		}(fund)
	}
	wg.Wait()
	data := gin.H{
		"Env":               viper.GetString("env"),
		"Version":           version.Version,
		"PageTitle":         "InvesTool | 基金 | 基金检测",
		"Funds":             funds,
		"StockCheckResults": stockCheckResults,
		"Param":             p,
	}
	c.JSON(http.StatusOK, data)
	return
}

// ParamFundSimilarity FundSimilarity 请求参数
type ParamFundSimilarity struct {
	Codes string `json:"codes" form:"codes"`
}

// FundSimilarity 基金持仓相似度
func FundSimilarity(c *gin.Context) {
	p := ParamFundSimilarity{}
	if err := c.ShouldBind(&p); err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 持仓相似度",
			"Error":     err.Error(),
		}
		c.HTML(http.StatusOK, "fund_similarity.html", data)
		return
	}
	if p.Codes == "" {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 持仓相似度",
			"Error":     "请填写待检测的基金代码",
		}
		c.HTML(http.StatusOK, "fund_similarity.html", data)
		return
	}
	codeList := goutils.SplitStringFields(p.Codes)
	checker := core.NewChecker(c, core.DefaultCheckerOptions)
	result, err := checker.GetFundStocksSimilarity(c, codeList)
	if err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 持仓相似度",
			"Error":     err.Error(),
		}
		c.HTML(http.StatusOK, "fund_similarity.html", data)
		return
	}
	data := gin.H{
		"Env":       viper.GetString("env"),
		"Version":   version.Version,
		"PageTitle": "InvesTool | 基金 | 持仓相似度",
		"Result":    result,
	}
	c.HTML(http.StatusOK, "fund_similarity.html", data)
	return
}

// ParamFundManagers 基金经理筛选参数
type ParamFundManagers struct {
	// 指定名字搜索
	Name string `json:"name" form:"name"`
	// 最低从业年限
	MinWorkingYears int `json:"min_working_years" form:"min_working_years"`
	// 最低年化回报（%）
	MinYieldse float64 `json:"min_yieldse" form:"min_yieldse"`
	// 最大现任基金数量
	MaxCurrentFundCount int `json:"max_current_fund_count" form:"max_current_fund_count"`
	// 最小管理规模（亿）
	MinScale float64 `json:"min_scale" form:"min_scale"`
	PageNum  int     `json:"page_num" form:"page_num"`
	PageSize int     `json:"page_size" form:"page_size"`
	Sort     string  `json:"sort" form:"sort"`
	FundType string  `json:"fund_type" form:"fund_type"`
}

// FundManagers godoc
func FundManagers(c *gin.Context) {
	p := ParamFundManagers{
		MinWorkingYears:     8,
		MinYieldse:          15.0,
		MaxCurrentFundCount: 10,
		MinScale:            60.0,
		PageNum:             1,
		PageSize:            10,
		Sort:                "yieldse",
		FundType:            "",
		Name:                "",
	}
	if err := c.ShouldBind(&p); err != nil {
		data := gin.H{
			"Env":       viper.GetString("env"),
			"Version":   version.Version,
			"PageTitle": "InvesTool | 基金 | 基金经理",
			"Error":     err.Error(),
		}
		c.HTML(http.StatusOK, "fund_managers.html", data)
		return
	}

	// 筛选
	managers := models.FundManagers.Filter(c, eastmoney.ParamFundManagerFilter{
		MinWorkingYears:     p.MinWorkingYears,
		MinYieldse:          p.MinYieldse,
		MaxCurrentFundCount: p.MaxCurrentFundCount,
		MinScale:            p.MinScale,
		FundType:            p.FundType,
	})

	// 排序
	switch p.Sort {
	case "yieldse":
		managers.SortByYieldse()
	case "scale":
		managers.SortByScale()
	case "score":
		managers.SortByScore()
	case "an":
		managers.SortByAwardNum()
	case "fc":
		managers.SortByFundCount()
	case "cbr":
		managers.SortByCurrentBestReturn()
	case "wbr":
		managers.SortByCurrentBestReturn()
	}

	// 分页
	pagi := goutils.PaginateByPageNumSize(len(managers), p.PageNum, p.PageSize)
	managers = managers[pagi.StartIndex:pagi.EndIndex]

	// 获取这批基金经理的代表基金是否是4433基金
	bestFundCodes := []string{}
	for _, m := range managers {
		bestFundCodes = append(bestFundCodes, m.CurrentBestFundCode)
	}
	searcher := core.NewSearcher(c)
	bestFundInfoMap, err := searcher.SearchFunds(c, bestFundCodes)
	if err != nil {
		logging.Error(c, "SearchFunds err:"+err.Error())
	}

	// 返回结果item
	type managerInfo struct {
		eastmoney.FundManagerInfo
		BestFundIs4433 bool
	}
	result := []managerInfo{}
	for _, m := range managers {
		i := bestFundInfoMap[m.CurrentBestFundCode]
		r := managerInfo{
			FundManagerInfo: *m,
			BestFundIs4433:  i.Is4433(c),
		}
		result = append(result, r)
	}

	data := gin.H{
		"Env":        viper.GetString("env"),
		"Version":    version.Version,
		"PageTitle":  "InvesTool | 基金 | 基金经理",
		"URLPath":    "/fund/managers",
		"Managers":   result,
		"Pagination": pagi,
		"Params":     p,
	}
	c.HTML(http.StatusOK, "fund_managers.html", data)
	return
}
