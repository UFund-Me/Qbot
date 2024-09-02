// 导出 json 文件

package cmds

import (
	"context"
	"encoding/json"
	"io/ioutil"
)

// ExportJSON 数据导出为 JSON 文件
// 不传文件名则返回 []bytes，传文件名则保存到文件
func (e Exportor) ExportJSON(ctx context.Context, filename string) (result []byte, err error) {
	result, err = json.MarshalIndent(e.Stocks, "", "  ")
	if filename != "" {
		err = ioutil.WriteFile(filename, result, 0666)
	}
	return
}
