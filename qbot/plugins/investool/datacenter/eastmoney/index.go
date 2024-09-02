// 指数信息

package eastmoney

import (
	"context"
	"fmt"

	"github.com/axiaoxin-com/goutils"
	"github.com/corpix/uarand"
)

// IndexData 指数信息
type IndexData struct {
	IndexCode     string      `json:"IndexCode"`
	IndexName     string      `json:"IndexName"`
	Newindextexch string      `json:"NEWINDEXTEXCH"`
	FullIndexName string      `json:"FullIndexName"`
	NewPrice      string      `json:"NewPrice"` // 指数点数
	NewPriceDate  string      `json:"NewPriceDate"`
	NewCHG        string      `json:"NewCHG"`     // 最新涨幅
	Reaprofile    string      `json:"reaprofile"` // 指数说明
	MakerName     string      `json:"MakerName"`  // 指数编制方
	Bkid          string      `json:"BKID"`
	BKName        string      `json:"BKName"` // 板块名称
	IsGuess       bool        `json:"IsGuess"`
	IndexvaluaCN  string      `json:"IndexvaluaCN"` // 估值：低估=-2，较为低估=-1，适中=0，较为高估=1，高估=2
	Petim         string      `json:"Petim"`        // 估值PE值
	Pep100        string      `json:"PEP100"`       // 估值PE百分位
	Pb            string      `json:"PB"`
	Pbp100        string      `json:"PBP100"`
	W             string      `json:"W"`   // 近一周涨幅
	M             string      `json:"M"`   // 近一月涨幅
	Q             string      `json:"Q"`   // 近三月涨幅
	Hy            string      `json:"HY"`  // 近六月涨幅
	Y             string      `json:"Y"`   // 近一年涨幅
	Twy           string      `json:"TWY"` // 近两年涨幅
	Try           string      `json:"TRY"` // 近三年涨幅
	Fy            string      `json:"FY"`  // 近五年涨幅
	Sy            string      `json:"SY"`  // 今年来涨幅
	StddevW       string      `json:"STDDEV_W"`
	StddevM       string      `json:"STDDEV_M"`
	StddevQ       string      `json:"STDDEV_Q"`
	StddevHy      string      `json:"STDDEV_HY"`
	StddevY       string      `json:"STDDEV_Y"`
	StddevTwy     string      `json:"STDDEV_TWY"`
	PDate         string      `json:"PDate"`
	TopicJJBID    interface{} `json:"TopicJJBId"`
	Isstatic      string      `json:"ISSTATIC"`
}

// IndexValueCN 指数估值
func (i *IndexData) IndexValueCN() string {
	switch i.IndexvaluaCN {
	case "-2":
		return "低估"
	case "-1":
		return "较为低估"
	case "0":
		return "适中"
	case "1":
		return "较为高估"
	case "2":
		return "高估"
	}
	return "--"
}

// RspIndex Index接口返回结构
type RspIndex struct {
	Datas        IndexData   `json:"Datas"`
	ErrCode      int         `json:"ErrCode"`
	Success      bool        `json:"Success"`
	ErrMsg       interface{} `json:"ErrMsg"`
	Message      interface{} `json:"Message"`
	ErrorCode    string      `json:"ErrorCode"`
	ErrorMessage interface{} `json:"ErrorMessage"`
	ErrorMsgLst  interface{} `json:"ErrorMsgLst"`
	TotalCount   int         `json:"TotalCount"`
	Expansion    interface{} `json:"Expansion"`
}

// Index 返回指数信息
func (e EastMoney) Index(ctx context.Context, indexCode string) (data *IndexData, err error) {
	apiurl := fmt.Sprintf(
		"https://fundztapi.eastmoney.com/FundSpecialApiNew/FundSpecialZSB30ZSIndex?IndexCode=%s&Version=6.5.5&deviceid=-&pageIndex=1&pageSize=10000&plat=Iphone&product=EFund",
		indexCode,
	)
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	rsp := RspIndex{}
	if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, &rsp); err != nil {
		return nil, err
	}
	if rsp.ErrCode != 0 {
		return nil, fmt.Errorf("Index rsp code error, rsp:%+v", rsp)
	}
	return &rsp.Datas, nil
}
