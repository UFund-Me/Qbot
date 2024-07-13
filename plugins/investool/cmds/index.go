package cmds

import (
	"fmt"
	"os"
	"strconv"

	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/logging"
	"github.com/olekukonko/tablewriter"
)

func showIndexData(data *eastmoney.IndexData) {
	table := tablewriter.NewWriter(os.Stdout)
	table.SetAlignment(tablewriter.ALIGN_LEFT)
	table.SetRowSeparator("")
	table.SetBorder(false)
	table.SetNoWhiteSpace(true)
	headers := []string{}
	table.SetHeader(headers)
	table.SetCaption(true, data.IndexCode+"指数信息")
	rows := [][]string{
		{"指数名称", data.FullIndexName},
		{"指数说明", data.Reaprofile},
		{"编制方", data.MakerName},
		{"估值", data.IndexValueCN()},
		{"估值PE值", data.Petim},
		{"估值PE百分位", data.Pep100},
		{"指数代码", data.IndexCode},
		{"板块名称", data.BKName},
		{"当前点数", data.NewPrice},
		{"最新涨幅", data.NewCHG},
		{"最近一周涨幅", data.W},
		{"最近一月涨幅", data.M},
		{"最近三月涨幅", data.Q},
		{"最近六月涨幅", data.Hy},
		{"最近一年涨幅", data.Y},
		{"最近两年涨幅", data.Twy},
		{"最近三年涨幅", data.Try},
		{"最近五年涨幅", data.Fy},
		{"今年来涨幅", data.Sy},
	}
	table.AppendBulk(rows)

	table.Render()
}

func showIndexStocks(stocks []eastmoney.ZSCFGItem) {
	table := tablewriter.NewWriter(os.Stdout)
	table.SetAlignment(tablewriter.ALIGN_LEFT)
	table.SetRowLine(true)
	headers := []string{"股票名称", "股票代码", "持仓占比"}
	table.SetHeader(headers)

	sum := 0.0
	for _, stock := range stocks {
		row := []string{stock.StockName, stock.StockCode, stock.Marketcappct}
		table.Append(row)
		if stock.Marketcappct != "" && stock.Marketcappct != "--" {
			v, err := strconv.ParseFloat(stock.Marketcappct, 64)
			if err != nil {
				logging.Error(nil, err.Error())
				continue
			}
			sum += v
		}
	}

	if len(stocks) > 0 {
		table.SetCaption(true, stocks[0].IndexName+"成分股")
	}
	footers := []string{fmt.Sprintf("总数:%d", len(stocks)), "--", fmt.Sprintf("占比求和:%.2f", sum)}
	table.SetFooter(footers)
	table.Render()
}

func showIntersecStocks(stocks1, stocks2 []eastmoney.ZSCFGItem) {
	table := tablewriter.NewWriter(os.Stdout)
	table.SetAlignment(tablewriter.ALIGN_LEFT)
	table.SetRowLine(true)
	headers := []string{"股票名称-代码"}
	table.SetHeader(headers)

	counter := map[string]int{}
	for _, stock := range stocks1 {
		key := fmt.Sprintf("%v-%v", stock.StockName, stock.StockCode)
		counter[key]++
	}

	for _, stock := range stocks2 {
		key := fmt.Sprintf("%v-%v", stock.StockName, stock.StockCode)
		counter[key]++
	}

	intersecCount := 0
	for k, v := range counter {
		if v == 2 {
			table.Append([]string{k})
			intersecCount++
		}
	}

	if intersecCount > 0 {
		table.SetCaption(true, fmt.Sprintf("%s∩%s 成分股交集", stocks1[0].IndexName, stocks2[0].IndexName))
	}
	footers := []string{fmt.Sprintf("交集总数:%d", intersecCount)}
	table.SetFooter(footers)
	table.Render()
}
