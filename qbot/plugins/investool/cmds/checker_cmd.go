// 检测器 cli command

package cmds

import (
	"context"
	"fmt"
	"strings"

	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/logging"
	"github.com/urfave/cli/v2"
)

const (
	// ProcessorChecker 检测器
	ProcessorChecker = "checker"
)

// FlagsChecker cli flags
func FlagsChecker() []cli.Flag {
	return []cli.Flag{
		&cli.StringFlag{
			Name:     "keyword",
			Aliases:  []string{"k"},
			Value:    "",
			Usage:    "检给定股票名称或代码，多个股票批量检测使用/分割。如: 招商银行/中国平安/600519",
			Required: true,
		},
	}
}

// FlagsCheckerOptions exportor checker flags
func FlagsCheckerOptions() []cli.Flag {
	return []cli.Flag{
		&cli.Float64Flag{
			Name:        "checker.min_roe",
			Value:       core.DefaultCheckerOptions.MinROE,
			Usage:       "最新一期 ROE 不低于该值",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MinROE),
		},
		&cli.IntFlag{
			Name:        "checker.check_years",
			Value:       core.DefaultCheckerOptions.CheckYears,
			Usage:       "连续增长年数",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.CheckYears),
		},
		&cli.Float64Flag{
			Name:        "checker.no_check_years_roe",
			Value:       core.DefaultCheckerOptions.NoCheckYearsROE,
			Usage:       "ROE 高于该值时不做连续增长检查",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.NoCheckYearsROE),
		},
		&cli.Float64Flag{
			Name:        "checker.max_debt_asset_ratio",
			Value:       core.DefaultCheckerOptions.MaxDebtAssetRatio,
			Usage:       "最大资产负债率百分比(%)",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MaxDebtAssetRatio),
		},
		&cli.Float64Flag{
			Name:        "checker.max_hv",
			Value:       core.DefaultCheckerOptions.MaxHV,
			Usage:       "最大历史波动率",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MaxHV),
		},
		&cli.Float64Flag{
			Name:        "checker.min_total_market_cap",
			Value:       core.DefaultCheckerOptions.MinTotalMarketCap,
			Usage:       "最小市值（亿）",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MinTotalMarketCap),
		},
		&cli.Float64Flag{
			Name:        "checker.bank_min_roa",
			Value:       core.DefaultCheckerOptions.BankMinROA,
			Usage:       "银行股最小 ROA",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.BankMinROA),
		},
		&cli.Float64Flag{
			Name:        "checker.bank_min_zbczl",
			Value:       core.DefaultCheckerOptions.BankMinZBCZL,
			Usage:       "银行股最小资本充足率",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.BankMinZBCZL),
		},
		&cli.Float64Flag{
			Name:        "checker.bank_max_bldkl",
			Value:       core.DefaultCheckerOptions.BankMaxBLDKL,
			Usage:       "银行股最大不良贷款率",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.BankMaxBLDKL),
		},
		&cli.Float64Flag{
			Name:        "checker.bank_min_bldkbbfgl",
			Value:       core.DefaultCheckerOptions.BankMinBLDKBBFGL,
			Usage:       "银行股最低不良贷款拨备覆盖率",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.BankMinBLDKBBFGL),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_mll_stability",
			Value:       core.DefaultCheckerOptions.IsCheckMLLStability,
			Usage:       "是否检测毛利率稳定性",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckMLLStability),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_jll_stability",
			Value:       core.DefaultCheckerOptions.IsCheckJLLStability,
			Usage:       "是否检测净利率稳定性",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckJLLStability),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_price_by_calc",
			Value:       core.DefaultCheckerOptions.IsCheckPriceByCalc,
			Usage:       "是否使用估算合理价进行检测，高于估算价将被过滤",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckPriceByCalc),
		},
		&cli.Float64Flag{
			Name:        "checker.max_peg",
			Value:       core.DefaultCheckerOptions.MaxPEG,
			Usage:       "最大 PEG",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MaxPEG),
		},
		&cli.Float64Flag{
			Name:        "checker.min_byys_ratio",
			Value:       core.DefaultCheckerOptions.MinBYYSRatio,
			Usage:       "最小本业营收比",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MinBYYSRatio),
		},
		&cli.Float64Flag{
			Name:        "checker.max_byys_ratio",
			Value:       core.DefaultCheckerOptions.MaxBYYSRatio,
			Usage:       "最大本业营收比",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MaxBYYSRatio),
		},
		&cli.Float64Flag{
			Name:        "checker.min_fzldb",
			Value:       core.DefaultCheckerOptions.MinFZLDB,
			Usage:       "最小负债流动比",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MinFZLDB),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_cashflow",
			Value:       core.DefaultCheckerOptions.IsCheckCashflow,
			Usage:       "是否检测现金流量",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckCashflow),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_mll_grow",
			Value:       core.DefaultCheckerOptions.IsCheckMLLGrow,
			Usage:       "是否检测毛利率逐年递增",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckMLLGrow),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_jll_grow",
			Value:       core.DefaultCheckerOptions.IsCheckJLLGrow,
			Usage:       "是否检测净利率逐年递增",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckJLLGrow),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_eps_grow",
			Value:       core.DefaultCheckerOptions.IsCheckEPSGrow,
			Usage:       "是否检测EPS逐年递增",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckEPSGrow),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_rev_grow",
			Value:       core.DefaultCheckerOptions.IsCheckRevGrow,
			Usage:       "是否检测营收逐年递增",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckRevGrow),
		},
		&cli.BoolFlag{
			Name:        "checker.is_check_netprofit_grow",
			Value:       core.DefaultCheckerOptions.IsCheckNetprofitGrow,
			Usage:       "是否检测净利润逐年递增",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.IsCheckNetprofitGrow),
		},
		&cli.Float64Flag{
			Name:        "checker.min_gxl",
			Value:       core.DefaultCheckerOptions.MinGxl,
			Usage:       "最低股息率",
			DefaultText: fmt.Sprint(core.DefaultCheckerOptions.MinGxl),
		},
	}
}

// NewCheckerOptions 从命令行参数解析 CheckerOptions
func NewCheckerOptions(c *cli.Context) core.CheckerOptions {
	checkerOpts := core.DefaultCheckerOptions
	checkerOpts.MinROE = c.Float64("checker.min_roe")
	checkerOpts.CheckYears = c.Int("checker.check_years")
	checkerOpts.NoCheckYearsROE = c.Float64("checker.no_check_years_roe")
	checkerOpts.MaxDebtAssetRatio = c.Float64("checker.max_debt_asset_ratio")
	checkerOpts.MaxHV = c.Float64("checker.max_hv")
	checkerOpts.MinTotalMarketCap = c.Float64("checker.min_total_market_cap")
	checkerOpts.BankMinROA = c.Float64("checker.bank_min_roa")
	checkerOpts.BankMinZBCZL = c.Float64("checker.bank_min_zbczl")
	checkerOpts.BankMaxBLDKL = c.Float64("checker.bank_max_bldkl")
	checkerOpts.BankMinBLDKBBFGL = c.Float64("checker.bank_min_bldkbbfgl")
	checkerOpts.IsCheckMLLStability = c.Bool("checker.is_check_mll_stability")
	checkerOpts.IsCheckJLLStability = c.Bool("checker.is_check_jll_stability")
	checkerOpts.IsCheckPriceByCalc = c.Bool("checker.is_check_price_by_calc")
	checkerOpts.MaxPEG = c.Float64("checker.max_peg")
	checkerOpts.MinBYYSRatio = c.Float64("checker.min_byys_ratio")
	checkerOpts.MaxBYYSRatio = c.Float64("checker.max_byys_ratio")
	checkerOpts.MinFZLDB = c.Float64("checker.min_fzldb")
	checkerOpts.IsCheckCashflow = c.Bool("checker.is_check_cashflow")
	checkerOpts.IsCheckMLLGrow = c.Bool("checker.is_check_mll_grow")
	checkerOpts.IsCheckJLLGrow = c.Bool("checker.is_check_jll_grow")
	checkerOpts.IsCheckEPSGrow = c.Bool("checker.is_check_eps_grow")
	checkerOpts.IsCheckRevGrow = c.Bool("checker.is_check_rev_grow")
	checkerOpts.IsCheckNetprofitGrow = c.Bool("checker.is_check_netprofit_grow")
	checkerOpts.MinGxl = c.Float64("checker.min_gxl")
	return checkerOpts
}

// ActionChecker cli action
func ActionChecker() func(c *cli.Context) error {
	return func(c *cli.Context) error {
		loglevel := c.String("loglevel")
		logging.SetLevel(loglevel)
		keyword := c.String("keyword")
		ctx := context.Background()
		keywords := strings.Split(keyword, "/")
		opts := NewCheckerOptions(c)
		Check(ctx, keywords, opts)
		return nil
	}
}

// CommandChecker 检测器 cli command
func CommandChecker() *cli.Command {
	flags := FlagsChecker()
	flags = append(flags, FlagsCheckerOptions()...)
	cmd := &cli.Command{
		Name:   ProcessorChecker,
		Usage:  "股票检测器",
		Flags:  flags,
		Action: ActionChecker(),
	}
	return cmd
}
