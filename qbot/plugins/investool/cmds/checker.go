// 对给定股票名/股票代码进行检测

package cmds

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/logging"
	"github.com/olekukonko/tablewriter"
)

// Check 对给定名称或代码进行检测，输出检测结果
func Check(ctx context.Context, keywords []string, opts core.CheckerOptions) (results map[string]core.CheckResult, err error) {
	results = make(map[string]core.CheckResult)
	searcher := core.NewSearcher(ctx)
	stocks, err := searcher.SearchStocks(ctx, keywords)
	if err != nil {
		logging.Fatal(ctx, err.Error())
	}

	for _, stock := range stocks {
		checker := core.NewChecker(ctx, opts)
		checkResult, ok := checker.CheckFundamentals(ctx, stock)
		k := fmt.Sprintf("%s-%s", stock.BaseInfo.SecurityNameAbbr, stock.BaseInfo.Secucode)
		results[k] = checkResult
		table := newTable()
		if !ok {
			renderTable(table, checkResult, []string{k, "FAILED"})
		} else {
			renderTable(table, checkResult, []string{k, "OK"})
		}
	}
	return results, nil
}

func newTable() *tablewriter.Table {
	table := tablewriter.NewWriter(os.Stdout)
	table.SetAlignment(tablewriter.ALIGN_LEFT)
	table.SetRowLine(true)
	headers := []string{"检测指标", "检测结果"}
	table.SetHeader(headers)
	table.SetHeaderColor(
		tablewriter.Colors{tablewriter.Bold, tablewriter.BgBlackColor},
		tablewriter.Colors{tablewriter.Bold, tablewriter.BgBlackColor},
	)
	return table
}

func renderTable(table *tablewriter.Table, checkResult core.CheckResult, footers []string) {
	footerValColor := tablewriter.FgRedColor
	if footers[1] == "OK" {
		footerValColor = tablewriter.FgGreenColor
	}
	table.SetFooter(footers)
	table.SetFooterColor(
		tablewriter.Colors{tablewriter.Bold, footerValColor},
		tablewriter.Colors{tablewriter.Bold, footerValColor},
	)
	for k, m := range checkResult {
		row := []string{k, strings.ReplaceAll(m["desc"], "<br/>", "\n")}

		if m["ok"] == "false" {
			table.Rich(
				row,
				[]tablewriter.Colors{{tablewriter.Bold, tablewriter.BgRedColor}, {tablewriter.Bold, tablewriter.BgRedColor}},
			)
		} else {
			table.Append(row)
		}
	}
	table.Render()
}
