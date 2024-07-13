// 导出结果为 excel

package cmds

import (
	"context"
	"encoding/json"
	"errors"
	"strings"
	"time"

	"github.com/360EntSecGroup-Skylar/excelize/v2"
	"github.com/axiaoxin-com/logging"
)

var (

	// HeaderStyle 表头样式
	HeaderStyle = &excelize.Style{
		Border: []excelize.Border{
			{Type: "left", Color: "000000", Style: 1},
			{Type: "right", Color: "000000", Style: 1},
			{Type: "top", Color: "000000", Style: 1},
			{Type: "bottom", Color: "000000", Style: 1},
		},
		Fill: excelize.Fill{
			Type:    "pattern",
			Pattern: 1,
			Color:   []string{"FFCCCC"},
			Shading: 0,
		},
		Font: &excelize.Font{
			Bold: true,
		},
		Alignment: &excelize.Alignment{
			Horizontal:      "center",
			JustifyLastLine: true,
			Vertical:        "center",
			WrapText:        true,
		},
	}
	// BodyStyle 表格Style
	BodyStyle = &excelize.Style{
		Alignment: &excelize.Alignment{
			Horizontal:      "left",
			JustifyLastLine: true,
			Vertical:        "center",
			WrapText:        true,
		},
	}
)

// ExportExcel 导出 excel
func (e Exportor) ExportExcel(ctx context.Context, filename string) (result []byte, err error) {
	stocksCount := len(e.Stocks)
	if stocksCount == 0 {
		err = errors.New("no stocks data")
		return
	}
	f := excelize.NewFile()

	// 创建全部数据表
	defaultSheet := "总览"
	lowPriceSheet := "30元内"
	hv1Sheet := "历史波动率低于1"
	hv2Sheet := "历史波动率高于1"
	sheets := []string{defaultSheet, lowPriceSheet, hv1Sheet, hv2Sheet}
	// 添加行业
	for _, industry := range e.Stocks.GetIndustryList() {
		sheets = append(sheets, industry+"行业")
	}

	headers := e.Stocks[0].GetHeaders()
	headersLen := len(headers)
	headerStyle, err := f.NewStyle(HeaderStyle)
	if err != nil {
		logging.Error(ctx, "New HeaderStyle error:"+err.Error())
	}
	bodyStyle, err := f.NewStyle(BodyStyle)
	if err != nil {
		logging.Error(ctx, "New BodyStyle error:"+err.Error())
	}
	// 创建 sheet
	for _, sheet := range sheets {
		if sheet == defaultSheet {
			f.SetSheetName("Sheet1", defaultSheet)
		}
		f.NewSheet(sheet)
		for i, header := range headers {
			// 设置列宽
			colNum := i + 1
			width := 30.0
			switch header {
			case "主营构成", "每股收益预测":
				width = 45.0
			case "公司信息":
				width = 65.0
			}
			col, err := excelize.ColumnNumberToName(colNum)
			if err != nil {
				logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
			}
			f.SetColWidth(sheet, col, col, width)
			// 设置表头行高
			rowNum := 1
			height := 20.0
			f.SetRowHeight(sheet, rowNum, height)
		}

		// 设置表头样式
		hcell, err := excelize.CoordinatesToCellName(1, 1)
		if err != nil {
			logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
			continue
		}
		vcell, err := excelize.CoordinatesToCellName(headersLen, 1)
		if err != nil {
			logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
			continue
		}
		f.SetCellStyle(sheet, hcell, vcell, headerStyle)

		// 设置表格样式
		hcell, err = excelize.CoordinatesToCellName(1, 2)
		if err != nil {
			logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
			continue
		}
		vcell, err = excelize.CoordinatesToCellName(headersLen, stocksCount+3)
		if err != nil {
			logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
			continue
		}
		f.SetCellStyle(sheet, hcell, vcell, bodyStyle)
	}

	// 开始写数据
	desc, _ := json.Marshal(map[string]interface{}{
		"筛选条件": e.Selector.Filter,
		"检测条件": e.Selector.Checker,
	})
	descStartCell, err := excelize.CoordinatesToCellName(1, stocksCount+3)
	if err != nil {
		logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
	}
	descEndCell, err := excelize.CoordinatesToCellName(headersLen, stocksCount+3)
	if err != nil {
		logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
	}
	for _, sheet := range sheets {
		// 写 header
		for i, header := range headers {
			axis, err := excelize.CoordinatesToCellName(i+1, 1)
			if err != nil {
				logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
				continue
			}
			f.SetCellValue(sheet, axis, header)
		}
		// 写 tail desc
		f.MergeCell(sheet, descStartCell, descEndCell)
		f.SetCellValue(sheet, descStartCell, "筛选条件: "+string(desc))
	}

	// 写 body
	for _, sheet := range sheets {
		row := 2
		for _, stock := range e.Stocks {
			switch sheet {
			case defaultSheet:
			case lowPriceSheet:
				if stock.Price > 30 {
					continue
				}
			case hv1Sheet:
				if stock.HV > 1 {
					continue
				}
			case hv2Sheet:
				if stock.HV <= 1 {
					continue
				}
			}
			if strings.HasSuffix(sheet, "行业") && !strings.Contains(sheet, stock.Industry) {
				continue
			}
			headerValueMap := stock.GetHeaderValueMap()
			for k, header := range headers {
				col := k + 1
				axis, err := excelize.CoordinatesToCellName(col, row)
				if err != nil {
					logging.Error(ctx, "CoordinatesToCellName error:"+err.Error())
					continue
				}
				value := headerValueMap[header]
				f.SetCellValue(sheet, axis, value)
			}
			row++
		}
	}
	f.SetDocProps(&excelize.DocProperties{
		Created:     time.Now().Format("2006-01-02 15:04:05"),
		Creator:     "axiaoxin",
		Description: string(desc),
		Keywords:    "investool: https://github.com/axiaoxin-com/investool",
	})

	buf, err := f.WriteToBuffer()
	result = buf.Bytes()
	err = f.SaveAs(filename)
	return
}
