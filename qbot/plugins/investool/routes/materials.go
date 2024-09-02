// 学习资料页面

package routes

import (
	"encoding/json"
	"net/http"

	"github.com/axiaoxin-com/investool/statics"
	"github.com/axiaoxin-com/investool/version"
	"github.com/axiaoxin-com/logging"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

// MaterialItem 学习资料具体信息
type MaterialItem struct {
	Name        string `json:"name"`
	DownloadURL string `json:"download_url"`
	Desc        string `json:"desc"`
}

// MaterialSeries 某一个系列的资料
// {
//     "飙股在线等": [
//         MaterialItem, ...
//     ]
// }
type MaterialSeries map[string][]MaterialItem

// TypedMaterialSeries 对MaterialSeries进行分类，如：视频、电子书等
// {
//     "videos": [
//         MaterialSeries, ...
//     ],
//     "ebooks": [
//         MaterialSeries, ...
//     ]
// }
type TypedMaterialSeries map[string][]MaterialSeries

// AllMaterialsList 包含全部资料信息的大JSON列表
// [
//     TypedMaterialSeries, ...
// ]
type AllMaterialsList []TypedMaterialSeries

// MaterialsFilename 资料JSON文件路径
var MaterialsFilename = "materials"

// Materials godoc
func Materials(c *gin.Context) {
	data := gin.H{
		"Env":       viper.GetString("env"),
		"Version":   version.Version,
		"PageTitle": "InvesTool | 资料",
	}
	f, err := statics.Files.ReadFile(MaterialsFilename)
	if err != nil {
		logging.Errorf(c, "Read MaterialsFilename:%v err:%v", MaterialsFilename, err)
		data["Error"] = err
		c.HTML(http.StatusOK, "materials.html", data)
		return
	}
	var mlist AllMaterialsList
	if err := json.Unmarshal(f, &mlist); err != nil {
		logging.Errorf(c, "json Unmarshal AllMaterialsList err:%v", err)
		data["Error"] = err
		c.HTML(http.StatusOK, "materials.html", data)
		return
	}
	data["AllMaterialsList"] = mlist
	c.HTML(http.StatusOK, "materials.html", data)
	return
}
