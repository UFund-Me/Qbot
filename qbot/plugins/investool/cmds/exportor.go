// 导出各类型的数据结果

package cmds

import (
	"context"
	"fmt"
	"os"
	"path"
	"strings"
	"time"

	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/logging"
)

// Exportor exportor 实例
type Exportor struct {
	Stocks   models.ExportorDataList
	Selector core.Selector
}

// New 创建要导出的数据列表
func New(ctx context.Context, stocks models.StockList, selector core.Selector) Exportor {
	dlist := models.ExportorDataList{}
	for _, s := range stocks {
		dlist = append(dlist, models.NewExportorData(ctx, s))
	}

	return Exportor{
		Stocks:   dlist,
		Selector: selector,
	}
}

// Export 导出数据
func Export(ctx context.Context, exportFilename string, selector core.Selector) {
	beginTime := time.Now()
	filedir := path.Dir(exportFilename)
	fileext := strings.ToLower(path.Ext(exportFilename))
	exportType := "excel"
	switch fileext {
	case ".json":
		exportType = "json"
	case ".csv", ".txt":
		exportType = "csv"
	case ".xlsx", ".xls":
		exportType = "excel"
	case ".png", ".jpg", ".jpeg", ".pic":
		exportType = "pic"
	case ".all":
		exportType = "all"
	}
	if _, err := os.Stat(filedir); os.IsNotExist(err) {
		os.Mkdir(filedir, 0755)
	}

	logging.Infof(ctx, "investool exportor start export selected stocks to %s", exportFilename)
	var err error
	// 自动筛选股票
	stocks, err := selector.AutoFilterStocks(ctx)
	if err != nil {
		logging.Fatal(ctx, err.Error())
	}
	e := New(ctx, stocks, selector)

	switch exportType {
	case "json":
		_, err = e.ExportJSON(ctx, exportFilename)
	case "csv":
		_, err = e.ExportCSV(ctx, exportFilename)
	case "excel":
		_, err = e.ExportExcel(ctx, exportFilename)
	case "pic":
		_, err = e.ExportPic(ctx, exportFilename)
	case "all":
		jsonFilename := strings.ReplaceAll(exportFilename, ".all", ".json")
		_, err = e.ExportJSON(ctx, jsonFilename)
		csvFilename := strings.ReplaceAll(exportFilename, ".all", ".csv")
		_, err = e.ExportCSV(ctx, csvFilename)
		xlsxFilename := strings.ReplaceAll(exportFilename, ".all", ".xlsx")
		_, err = e.ExportExcel(ctx, xlsxFilename)
		pngFilename := strings.ReplaceAll(exportFilename, ".all", ".png")
		_, err = e.ExportPic(ctx, pngFilename)
	}
	if err != nil {
		logging.Fatal(ctx, err.Error())
	}

	fmt.Printf(
		"\ninvestool exportor export %s succuss, total:%d latency:%#vs\n",
		exportType,
		len(stocks),
		time.Now().Sub(beginTime).Seconds(),
	)
}
