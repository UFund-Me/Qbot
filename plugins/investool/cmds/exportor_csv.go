// 导出 csv

package cmds

import (
	"context"
	"io/ioutil"

	"github.com/gocarina/gocsv"
)

// ExportCSV 数据导出为 CSV
// 不传文件名则返回 []bytes，传文件名则保存到文件
func (e Exportor) ExportCSV(ctx context.Context, filename string) (result []byte, err error) {
	result, err = gocsv.MarshalBytes(&e.Stocks)

	if filename != "" {
		err = ioutil.WriteFile(filename, result, 0666)
	}
	return
}
