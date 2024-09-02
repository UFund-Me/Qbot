// 导出器 cli command

package cmds

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/logging"
	"github.com/urfave/cli/v2"
)

const (
	// ProcessorExportor 导出器
	ProcessorExportor = "exportor"
)

var (
	// DefaultExportFilename 要导出的文件名默认值
	DefaultExportFilename = fmt.Sprintf("./dist/investool.%s.xlsx", time.Now().Format("20060102"))
)

// FlagsExportor exportor cli flags
func FlagsExportor() []cli.Flag {
	return []cli.Flag{
		&cli.StringFlag{
			Name:        "filename",
			Aliases:     []string{"f"},
			Value:       DefaultExportFilename,
			Usage:       `指定导出文件名`,
			EnvVars:     []string{"XSTOCK_EXPORTOR_FILENAME"},
			DefaultText: DefaultExportFilename,
		},
		&cli.BoolFlag{
			Name:        "disable_check",
			Aliases:     []string{"C"},
			Value:       false,
			Usage:       "关闭基本面检测，导出所有原始筛选结果",
			EnvVars:     []string{"XSTOCK_EXPORTOR_DISABLE_CHECK"},
			DefaultText: "false",
		},
	}
}

// FlagsFilter exportor filter flag
func FlagsFilter() []cli.Flag {
	return []cli.Flag{
		&cli.Float64Flag{
			Name:        "filter.min_roe",
			Value:       8.0,
			Usage:       "最低净资产收益率 (%)",
			DefaultText: "8.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_netprofit_yoy_ratio",
			Value:       0.0,
			Usage:       "最低净利润增长率 (%)",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_toi_yoy_ratio",
			Value:       0.0,
			Usage:       "最低营收增长率 (%)",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_zxgxl",
			Value:       0.0,
			Usage:       "最低最新股息率 (%)",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_netprofit_growthrate_3_y",
			Value:       0.0,
			Usage:       "最低净利润 3 年复合增长率（%）",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_income_growthrate_3_y",
			Value:       0.0,
			Usage:       "最低营收 3 年复合增长率（%）",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_listing_yield_year",
			Value:       0.0,
			Usage:       "最低上市以来年化收益率（%）",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_pb_new_mrq",
			Value:       1.0,
			Usage:       "最低市净率",
			DefaultText: "1.0",
		},
		&cli.Float64Flag{
			Name:        "filter.max_debt_asset_ratio",
			Value:       0.0,
			Usage:       "最大资产负债率 (%)",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_predict_netprofit_ratio",
			Value:       0.0,
			Usage:       "最低预测净利润同比增长（%）",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_predict_income_ratio",
			Value:       0.0,
			Usage:       "最低预测营收同比增长（%）",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_total_market_cap",
			Value:       100.0,
			Usage:       "最低总市值（亿）",
			DefaultText: "100.0",
		},
		&cli.StringSliceFlag{
			Name:        "filter.industry_list",
			Value:       cli.NewStringSlice(),
			Usage:       "行业名",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.min_price",
			Value:       0.0,
			Usage:       "股价范围最小值（元）",
			DefaultText: "0.0",
		},
		&cli.Float64Flag{
			Name:        "filter.max_price",
			Value:       0.0,
			Usage:       "股价范围最大值（元）",
			DefaultText: "0.0",
		},
		&cli.BoolFlag{
			Name:        "filter.listing_over_5_y",
			Value:       false,
			Usage:       "上市时间是否超过 5 年",
			DefaultText: "false",
		},
		&cli.Float64Flag{
			Name:        "filter.min_listing_volatility_year",
			Value:       0.0,
			Usage:       "最低上市以来年化波动率",
			DefaultText: "0.0",
		},
		&cli.BoolFlag{
			Name:        "filter.exclude_cyb",
			Value:       true,
			Usage:       "排除创业板",
			DefaultText: "true",
		},
		&cli.BoolFlag{
			Name:        "filter.exclude_kcb",
			Value:       true,
			Usage:       "排除科创板",
			DefaultText: "true",
		},
		&cli.StringSliceFlag{
			Name:        "filter.special_security_name_abbr_list",
			Value:       cli.NewStringSlice(),
			Usage:       "查询指定名称",
			DefaultText: "",
		},
		&cli.StringSliceFlag{
			Name:        "filter.special_security_code_list",
			Value:       cli.NewStringSlice(),
			Usage:       "查询指定代码",
			DefaultText: "",
		},
		&cli.Float64Flag{
			Name:        "filter.min_roa",
			Value:       0.0,
			Usage:       "最小总资产收益率 ROA",
			DefaultText: "0.0",
		},
	}
}

// NewFilter 从命令行解析 filter 参数
func NewFilter(c *cli.Context) eastmoney.Filter {
	filter := eastmoney.DefaultFilter
	filter.MinROE = c.Float64("filter.min_roe")
	filter.MinNetprofitYoyRatio = c.Float64("filter.min_netprofit_yoy_ratio")
	filter.MinToiYoyRatio = c.Float64("filter.min_toi_yoy_ratio")
	filter.MinZXGXL = c.Float64("filter.min_zxgxl")
	filter.MinNetprofitGrowthrate3Y = c.Float64("filter.min_netprofit_growthrate_3_y")
	filter.MinIncomeGrowthrate3Y = c.Float64("filter.min_income_growthrate_3_y")
	filter.MinListingYieldYear = c.Float64("filter.min_listing_yield_year")
	filter.MinPBNewMRQ = c.Float64("filter.min_pb_new_mrq")
	filter.MaxDebtAssetRatio = c.Float64("filter.max_debt_asset_ratio")
	filter.MinPredictNetprofitRatio = c.Float64("filter.min_predict_netprofit_ratio")
	filter.MinPredictIncomeRatio = c.Float64("filter.min_predict_income_ratio")
	filter.MinTotalMarketCap = c.Float64("filter.min_total_market_cap")
	filter.IndustryList = c.StringSlice("filter.industry_list")
	filter.MinPrice = c.Float64("filter.min_price")
	filter.MaxPrice = c.Float64("filter.max_price")
	filter.ListingOver5Y = c.Bool("filter.listing_over_5_y")
	filter.MinListingVolatilityYear = c.Float64("filter.min_listing_volatility_year")
	filter.ExcludeCYB = c.Bool("filter.exclude_cyb")
	filter.ExcludeKCB = c.Bool("filter.exclude_kcb")
	filter.SpecialSecurityNameAbbrList = c.StringSlice("filter.special_security_name_abbr_list")
	filter.SpecialSecurityCodeList = c.StringSlice("filter.special_security_code_list")
	filter.MinROA = c.Float64("filter.min_roa")
	return filter
}

// ActionExportor cli action
func ActionExportor() func(c *cli.Context) error {
	return func(c *cli.Context) error {
		ctx := context.Background()
		loglevel := c.String("loglevel")
		logging.SetLevel(loglevel)

		checkerOpts := NewCheckerOptions(c)
		checker := core.NewChecker(ctx, checkerOpts)
		if c.Bool("disable_check") {
			checker = nil
		}
		filter := NewFilter(c)
		selector := core.NewSelector(ctx, filter, checker)
		b, _ := json.MarshalIndent(map[string]interface{}{
			"filter":  filter,
			"checker": checker,
		}, "", "  ")
		logging.Debug(ctx, "exportor params:"+string(b))
		Export(ctx, c.String("filename"), selector)
		return nil
	}
}

// CommandExportor 导出器 cli command
func CommandExportor() *cli.Command {
	flags := FlagsExportor()
	flags = append(flags, FlagsFilter()...)
	flags = append(flags, FlagsCheckerOptions()...)
	cmd := &cli.Command{
		Name:      ProcessorExportor,
		Usage:     "股票筛选导出器",
		UsageText: "将按条件筛选出的股票导出到文件，根据文件后缀名自动判断导出类型。支持的后缀名：[xlsx|csv|json|png|all]，all 表示导出全部支持的类型。",
		Flags:     flags,
		Action:    ActionExportor(),
	}
	return cmd
}
