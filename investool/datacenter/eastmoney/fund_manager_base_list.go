// 天天基金获取基金经理列表

package eastmoney

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/corpix/uarand"
	"go.uber.org/zap"
)

// FundManagerBaseInfo 基金经理基本信息
type FundManagerBaseInfo struct {
	// ID
	Mgrid string `json:"MGRID"`
	// 姓名
	Mgrname string `json:"MGRNAME"`
	// 擅长领域 1:偏债类 2:偏股类 3:指数类 4:货币类 5:QDII
	Mftype string `json:"MFTYPE"`
	// 基金公司
	Jjgs string `json:"JJGS"`
	// 基金公司id
	Jjgsid string `json:"JJGSID"`
	// 从业年化收益（%）
	Yieldse string `json:"YIELDSE"`
	// 近1周涨跌幅（%）
	W string `json:"W"`
	// 近1月涨跌幅（%）
	M string `json:"M"`
	// 近3月涨跌幅（%）
	Q string `json:"Q"`
	// 近6月涨跌幅（%）
	Hy string `json:"HY"`
	// 近1年涨跌幅（%）
	Y string `json:"Y"`
	// 管理规模（元）
	Netnav string `json:"NETNAV"`
	// 业绩评分
	Mgold string `json:"MGOLD"`
	// 代表基金代码
	Precode string `json:"PRECODE"`
	// 代表基金名称
	Shortname string `json:"SHORTNAME"`
	// 头像
	Newphotourl string `json:"NEWPHOTOURL"`
	// 性别 0:男 1:女
	Sex string `json:"SEX"`
}

// MftypeDesc Mftype字段描述
var MftypeDesc = map[string]string{
	"1": "偏债类",
	"2": "偏股类",
	"3": "指数类",
	"4": "货币类",
	"5": "QDII",
}

// RespFundMangerBaseList FundMangerBaseList 接口原始返回结构
type RespFundMangerBaseList struct {
	Datas      []*FundManagerBaseInfo `json:"Datas"`
	ErrCode    int                    `json:"ErrCode"`
	ErrMsg     interface{}            `json:"ErrMsg"`
	TotalCount int                    `json:"TotalCount"`
	Expansion  interface{}            `json:"Expansion"`
}

// FundMangerBaseList 查询基金经理列表（app接口）
// mftype "":全部 1:偏债类 2:偏股类 3:指数类 4:货币类 5:QDII
// sortColum W:近1周平均收益 M:近1月平均收益 Q:近3月平均收益 HY:近半年平均收益 Y:近1年平均收益 NETNAV:管理规模 MGOLD:业绩评价 YIELDSE:从业年化回报
func (e EastMoney) FundMangerBaseList(ctx context.Context, mftype string, sortColum string) ([]*FundManagerBaseInfo, error) {
	beginTime := time.Now()
	resp := RespFundMangerBaseList{}
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	// TODO: 并发优化
	result := []*FundManagerBaseInfo{}
	index := 1
	size := 300
	total := 0
	for {
		apiurl := fmt.Sprintf(
			"https://fundmapi.eastmoney.com/fundmobapi/FundMApi/FundMangerBaseList.ashx?COMPANYCODES=&MFTYPE=%s&Sort=desc&SortColumn=%s&deviceid=fundmanager2016&pageIndex=%d&pageSize=%d&plat=Iphone&product=EFund&version=4.3.0",
			mftype,
			sortColum,
			index,
			size,
		)
		logging.Debug(ctx, "EastMoney FundMangerBaseList "+apiurl+" begin", zap.Int("index", index))
		if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, &resp); err != nil {
			return nil, err
		}
		total = resp.TotalCount
		if len(resp.Datas) == 0 {
			break
		}
		result = append(result, resp.Datas...)
		index++
	}
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney FundMangerBaseList end",
		zap.Int64("latency(ms)", latency),
		zap.Int("totalCount", total),
		zap.Int("resultCount", len(result)),
	)
	return result, nil
}

// RespFundMsnManagerInfo FundMsnManagerInfo接口返回结构
type RespFundMsnManagerInfo struct {
	Datas struct {
		Mgrid            string `json:"MGRID"`
		Mgrname          string `json:"MGRNAME"`
		Resume           string `json:"RESUME"`
		Investmentmethod string `json:"INVESTMENTMETHOD"`
		Investmentidear  string `json:"INVESTMENTIDEAR"`
		Totaldays        string `json:"TOTALDAYS"`
		Netnav           string `json:"NETNAV"`
		Fcount           string `json:"FCOUNT"`
		Tcount           string `json:"TCOUNT"`
		Precode          string `json:"PRECODE"`
		Prename          string `json:"PRENAME"`
		Awardnum         string `json:"AWARDNUM"`
		Iswxpj           string `json:"ISWXPJ"`
		Pf3              string `json:"PF_3"`
		Yj3              string `json:"YJ_3"`
		Maxpenavgrowth   string `json:"MAXPENAVGROWTH"`
		Yieldse          string `json:"YIELDSE"`
		Jjgs             string `json:"JJGS"`
		Jjgsid           string `json:"JJGSID"`
		Newphotourl      string `json:"NEWPHOTOURL"`
		Mftype           string `json:"MFTYPE"`
		AwardnumJn       string `json:"AWARDNUM_JN"`
		AwardnumMx       string `json:"AWARDNUM_MX"`
		Awardfnum        string `json:"AWARDFNUM"`
		Fcode            string `json:"FCODE"`
		Shortname        string `json:"SHORTNAME"`
		Maxretra1        string `json:"MAXRETRA1"`
		Maxearn1         string `json:"MAXEARN1"`
		Fmaxearn1        string `json:"FMAXEARN1"`
		Fmaxretra1       string `json:"FMAXRETRA1"`
		Sex              string `json:"SEX"`
		Wins             []struct {
			Fcode         string `json:"FCODE"`
			Shortname     string `json:"SHORTNAME"`
			Awardfullname string `json:"AWARDFULLNAME"`
			Awardname     string `json:"AWARDNAME"`
			Noticedate    string `json:"NOTICEDATE"`
		} `json:"WINS"`
		Mgold  string `json:"MGOLD"`
		Sday   string `json:"SDAY"`
		Sct1   string `json:"SCT1"`
		Sstd1  string `json:"SSTD1"`
		Srt1   string `json:"SRT1"`
		Sy1    string `json:"SY1"`
		Sinfo1 string `json:"SINFO1"`
		Strk1  string `json:"STRK1"`
		Snav   string `json:"SNAV"`
		Sgr    string `json:"SGR"`
	} `json:"Datas"`
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

// QueryFundMsnMangerInfo 查询基金经理信息（app接口）
func (e EastMoney) QueryFundMsnMangerInfo(ctx context.Context, mgrid string) (*RespFundMsnManagerInfo, error) {
	beginTime := time.Now()
	resp := &RespFundMsnManagerInfo{}
	apiurl := fmt.Sprintf(
		"https://fundztapi.eastmoney.com/FundSpecialApiNew/FundMSNMangerInfo?FCODE=%s&plat=Iphone&deviceid=123&product=EFund&version=6.4.7",
		mgrid,
	)
	logging.Debug(ctx, "EastMoney QueryFundMsnMangerInfo "+apiurl+" begin")
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	if err := goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, resp); err != nil {
		return nil, err
	}
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFundMsnMangerInfo end",
		zap.Int64("latency(ms)", latency),
	)

	if resp.ErrCode != 0 {
		return nil, errors.New(resp.ErrMsg.(string))
	}

	return resp, nil
}
