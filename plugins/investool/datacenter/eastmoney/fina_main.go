// 获取财报数据

package eastmoney

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"go.uber.org/zap"
)

// FinaMainData 财报主要指标
type FinaMainData struct {
	// 股票代码: 111111.SZ
	Secucode string `json:"SECUCODE"`
	// 股票代码: 111111
	SecurityCode string `json:"SECURITY_CODE"`
	// 股票名称
	SecurityNameAbbr string `json:"SECURITY_NAME_ABBR"`
	OrgCode          string `json:"ORG_CODE"`
	OrgType          string `json:"ORG_TYPE"`
	// 报告期
	ReportDate string `json:"REPORT_DATE"`
	// 财报类型：年报、三季报、中报、一季报
	ReportType FinaReportType `json:"REPORT_TYPE"`
	// 财报名称: 2021 一季报
	ReportDateName string `json:"REPORT_DATE_NAME"`
	// 财报年份： 2021
	ReportYear       string `json:"REPORT_YEAR"`
	SecurityTypeCode string `json:"SECURITY_TYPE_CODE"`
	NoticeDate       string `json:"NOTICE_DATE"`
	// 财报更新时间
	UpdateDate string `json:"UPDATE_DATE"`
	// 货币类型： CNY
	Currency string `json:"CURRENCY"`

	// ------ 每股指标 ------
	// 基本每股收益（元）
	Epsjb float64 `json:"EPSJB"`
	// 基本每股收益同比增长（%）
	Epsjbtz float64 `json:"EPSJBTZ"`
	// 扣非每股收益（元）
	Epskcjb float64 `json:"EPSKCJB"`
	// 稀释每股收益（元）
	Epsxs float64 `json:"EPSXS"`
	// 每股净资产（元）
	Bps float64 `json:"BPS"`
	// 每股净资产同比增长（%）
	Bpstz float64 `json:"BPSTZ"`
	// 每股资本公积（元）
	Mgzbgj float64 `json:"MGZBGJ"`
	// 每股资本公积同比增长（%）
	Mgzbgjtz float64 `json:"MGZBGJTZ"`
	// 每股未分配利润（元）
	Mgwfplr float64 `json:"MGWFPLR"`
	// 每股未分配利润同比增长（%）
	Mgwfplrtz float64 `json:"MGWFPLRTZ"`
	// 每股经营现金流（元）
	Mgjyxjje float64 `json:"MGJYXJJE"`
	// 每股经营现金流同比增长（%）
	Mgjyxjjetz float64 `json:"MGJYXJJETZ"`

	// ------ 成长能力指标 ------
	// 营业总收入（元）
	Totaloperatereve float64 `json:"TOTALOPERATEREVE"`
	// 营业总收入同比增长（%）
	Totaloperaterevetz float64 `json:"TOTALOPERATEREVETZ"`
	// 毛利润（元）
	Mlr float64 `json:"MLR"`
	// 归属净利润（元）
	Parentnetprofit float64 `json:"PARENTNETPROFIT"`
	// 归属净利润同比增长（%）
	Parentnetprofittz float64 `json:"PARENTNETPROFITTZ"`
	// 扣非净利润（元）
	Kcfjcxsyjlr float64 `json:"KCFJCXSYJLR"`
	// 扣非净利润同比增长（%）
	Kcfjcxsyjlrtz float64 `json:"KCFJCXSYJLRTZ"`
	// 营业总收入滚动环比增长（%）
	Yyzsrgdhbzc float64 `json:"YYZSRGDHBZC"`
	// 归属净利润滚动环比增长（%）
	Netprofitrphbzc float64 `json:"NETPROFITRPHBZC"`
	// 扣非净利润滚动环比增长（%）
	Kfjlrgdhbzc float64 `json:"KFJLRGDHBZC"`

	// ------ 盈利能力指标 ------
	// 净资产收益率（加权）（%）
	Roejq float64 `json:"ROEJQ"`
	// 净资产收益率（扣非/加权）（%）
	Roekcjq float64 `json:"ROEKCJQ"`
	// 净资产收益率同比增长（%）
	Roejqtz float64 `json:"ROEJQTZ"`
	// 总资产收益率（加权） ROA （%）
	Zzcjll float64 `json:"ZZCJLL"`
	// 总资产收益率同比增长（%）
	Zzcjlltz float64 `json:"ZZCJLLTZ"`
	// 投入资本回报率（%）
	Roic float64 `json:"ROIC"`
	// 投入资本回报率同比增长（%）
	Roictz float64 `json:"ROICTZ"`
	// 毛利率（%）
	Xsmll float64 `json:"XSMLL"`
	// 净利率（%）
	Xsjll float64 `json:"XSJLL"`

	// ------ 收益质量指标 ------
	// 预收账款/营业收入
	Yszkyysr interface{} `json:"YSZKYYSR"`
	// 销售净现金流/营业收入
	Xsjxlyysr float64 `json:"XSJXLYYSR"`
	// 经营净现金流/营业收入
	Jyxjlyysr float64 `json:"JYXJLYYSR"`
	// 实际税率（%）
	Taxrate float64 `json:"TAXRATE"`

	// ------ 财务风险指标 ------
	// 流动比率
	Ld float64 `json:"LD"`
	// 速动比率
	Sd float64 `json:"SD"`
	// 现金流量比率
	Xjllb float64 `json:"XJLLB"`
	// 资产负债率（%）
	Zcfzl float64 `json:"ZCFZL"`
	// 资产负债率同比增长（%）
	Zcfzltz float64 `json:"ZCFZLTZ"`
	// 权益乘数
	Qycs float64 `json:"QYCS"`
	// 产权比率
	Cqbl float64 `json:"CQBL"`

	// ------ 营运能力指标 ------
	// 总资产周转天数（天）
	Zzczzts float64 `json:"ZZCZZTS"`
	// 存货周转天数（天）
	Chzzts float64 `json:"CHZZTS"`
	// 应收账款周转天数（天）
	Yszkzzts float64 `json:"YSZKZZTS"`
	// 总资产周转率（次）
	Toazzl float64 `json:"TOAZZL"`
	// 存货周转率（次）
	Chzzl float64 `json:"CHZZL"`
	// 应收账款周转率（次）
	Yszkzzl float64 `json:"YSZKZZL"`

	// ------ 银行股专项指标 ------
	// 存款总额
	TotalDeposits float64 `json:"TOTALDEPOSITS"`
	// 贷款总额
	GrossLoans float64 `json:"GROSSLOANS"`
	// 存贷款比例
	Ltdrr float64 `json:"LTDRR"`
	// 资本充足率
	Newcapitalader float64 `json:"NEWCAPITALADER"`
	// 核心资产充足率
	Hxyjbczl float64 `json:"HXYJBCZL"`
	// 不良贷款率
	NonPerLoan float64 `json:"NONPERLOAN"`
	// 不良贷款拨备覆盖率
	Bldkbbl float64 `json:"BLDKBBL"`
	// 资本净额
	Nzbje float64 `json:"NZBJE"`

	// ------ 保险股专项指标 ------
	// 总投资收益率
	TotalRoi float64 `json:"TOTAL_ROI"`
	// 净投资收益率
	NetRoi float64 `json:"NET_ROI"`
	// 已赚保费
	EarnedPremium float64 `json:"EARNED_PREMIUM"`
	// 赔付支出
	CompensateExpense float64 `json:"COMPENSATE_EXPENSE"`
	// 退保率
	SurrenderRateLife float64 `json:"SURRENDER_RATE_LIFE"`
	// 偿付能力充足率
	SolvencyAr float64 `json:"SOLVENCY_AR"`
	// 新业务价值（寿险）
	NbvLife float64 `json:"NBV_LIFE"`
	// 新业务价值率（寿险）
	NbvRate float64 `json:"NBV_RATE"`
	// 内含价值（寿险）
	NhjzCurrentAmt float64 `json:"NHJZ_CURRENT_AMT"`
}

// HistoricalFinaMainData 主要指标历史数据列表
type HistoricalFinaMainData []FinaMainData

// FinaReportType 财报类型
type FinaReportType string

const (
	// FinaReportTypeQ1 一季报
	FinaReportTypeQ1 FinaReportType = "一季报"
	// FinaReportTypeMid 中报
	FinaReportTypeMid FinaReportType = "中报"
	// FinaReportTypeQ3 三季报
	FinaReportTypeQ3 FinaReportType = "三季报"
	// FinaReportTypeYear 年报
	FinaReportTypeYear FinaReportType = "年报"
)

// FilterByReportType 按财报类型过滤：一季报，中报，三季报，年报
func (h HistoricalFinaMainData) FilterByReportType(ctx context.Context, reportType FinaReportType) HistoricalFinaMainData {
	result := HistoricalFinaMainData{}
	for _, i := range h {
		if i.ReportType == reportType {
			result = append(result, i)
		}
	}
	return result
}

// FilterByReportYear 按财报年份过滤： 2021
func (h HistoricalFinaMainData) FilterByReportYear(ctx context.Context, reportYear int) HistoricalFinaMainData {
	result := HistoricalFinaMainData{}
	year := fmt.Sprint(reportYear)
	for _, i := range h {
		if i.ReportYear == year {
			result = append(result, i)
		}
	}
	return result
}

// GetReport 获取指定年份+季度的财报
func (h HistoricalFinaMainData) GetReport(ctx context.Context, reportYear int, reportType FinaReportType) *FinaMainData {
	year := fmt.Sprint(reportYear)
	for _, i := range h {
		if i.ReportYear == year && i.ReportType == reportType {
			return &i
		}
	}
	return nil
}

// CurrentReport 当前最新一期财报
func (h HistoricalFinaMainData) CurrentReport(ctx context.Context) *FinaMainData {
	if len(h) > 0 {
		return &h[0]
	}
	return nil
}

// PreviousReport 当前上一期财报
func (h HistoricalFinaMainData) PreviousReport(ctx context.Context) *FinaMainData {
	if len(h) > 1 {
		return &h[1]
	}
	return nil
}

// ValueListType 列表数据的数据类型
type ValueListType string

const (
	// ValueListTypeNetProfit 净利润
	ValueListTypeNetProfit ValueListType = "NETPROFIT"
	// ValueListTypeGrossProfit 毛利润
	ValueListTypeGrossProfit ValueListType = "GROSSPROFIT"
	// ValueListTypeRevenue 营收
	ValueListTypeRevenue ValueListType = "REVENUE"
	// ValueListTypeROE roe
	ValueListTypeROE ValueListType = "ROE"
	// ValueListTypeEPS eps
	ValueListTypeEPS ValueListType = "EPS"
	// ValueListTypeROA roa
	ValueListTypeROA ValueListType = "ROA"
	// ValueListTypeMLL 毛利率
	ValueListTypeMLL ValueListType = "MLL"
	// ValueListTypeJLL 净利率
	ValueListTypeJLL ValueListType = "JLL"
)

// FinaValueList 历史数据值列表
type FinaValueList []float64

func (fvl FinaValueList) String() string {
	s := []string{}
	for _, i := range fvl {
		s = append(s, fmt.Sprint(i))
	}
	return strings.Join(s, "<br>")
}

// ValueList 获取历史数据值，最新的在最前面
func (h HistoricalFinaMainData) ValueList(
	ctx context.Context,
	valueType ValueListType,
	count int,
	reportType FinaReportType,
) FinaValueList {
	r := []float64{}
	data := h.FilterByReportType(ctx, reportType)
	dataLen := len(data)
	if dataLen == 0 {
		return r
	}
	if count > 0 {
		if count > dataLen {
			count = dataLen
		}
		data = data[:count]
	}
	for _, i := range data {
		value := float64(-1)
		switch valueType {
		case ValueListTypeNetProfit:
			value = i.Parentnetprofit
		case ValueListTypeGrossProfit:
			value = i.Mlr
		case ValueListTypeRevenue:
			value = i.Totaloperatereve
		case ValueListTypeEPS:
			value = i.Epsjb
		case ValueListTypeROA:
			value = i.Zzcjll
		case ValueListTypeROE:
			value = i.Roejq
		case ValueListTypeMLL:
			value = i.Xsmll
		case ValueListTypeJLL:
			value = i.Xsjll
		}
		r = append(r, value)
	}
	return r
}

// IsIncreasingByYears roe/eps/revenue/profit 是否逐年递增
func (h HistoricalFinaMainData) IsIncreasingByYears(
	ctx context.Context,
	valueType ValueListType,
	yearsCount int,
	reportType FinaReportType,
) bool {
	data := h.ValueList(ctx, valueType, yearsCount, reportType)
	increasing := true
	for i := 0; i < len(data)-1; i++ {
		if data[i] <= data[i+1] {
			increasing = false
			break
		}
	}
	return increasing
}

// IsStability 数据是否稳定（标准差在 1 以内）
func (h HistoricalFinaMainData) IsStability(
	ctx context.Context,
	valueType ValueListType,
	yearsCount int,
	reportType FinaReportType,
) bool {
	values := h.ValueList(ctx, valueType, yearsCount, reportType)
	sd, err := goutils.StdDeviationFloat64(values)
	if err != nil {
		logging.Error(ctx, "IsStability StdDeviationFloat64 error:"+err.Error())
		return false
	}
	logging.Debugf(ctx, "StdDeviation value:%v", sd)
	// 2.51 这个值是取了37家银行的标准差的平均值作为标准
	return sd <= 2.51
}

// MidValue 历史年报 roe/eps 中位数
func (h HistoricalFinaMainData) MidValue(
	ctx context.Context,
	valueType ValueListType,
	yearsCount int,
	reportType FinaReportType,
) (float64, error) {
	data := h.ValueList(ctx, valueType, yearsCount, reportType)
	return goutils.MidValueFloat64(data)
}

// GetAvgRevenueIncreasingRatioByYear 获取指定年内已发布的各期财报的平均营收同比增长比 (%)
func (h HistoricalFinaMainData) GetAvgRevenueIncreasingRatioByYear(ctx context.Context, year int) float64 {
	data := h.FilterByReportYear(ctx, year)
	dlen := len(data)
	if dlen == 0 {
		return 0
	}
	sum := 0.0
	for _, d := range data {
		sum += d.Totaloperaterevetz
	}

	return sum / float64(dlen)
}

// GetAvgEpsIncreasingRatioByYear 获取指定年内已发布的各期财报的平均EPS同比增长比 (%)
func (h HistoricalFinaMainData) GetAvgEpsIncreasingRatioByYear(ctx context.Context, year int) float64 {
	data := h.FilterByReportYear(ctx, year)
	dlen := len(data)
	if dlen == 0 {
		return 0
	}
	sum := 0.0
	for _, d := range data {
		sum += d.Epsjbtz
	}

	return sum / float64(dlen)
}

// GetAvgParentNetprofitIncreasingRatioByYear 获取指定年内已发布的各期财报的平均归属净利润同比增长比 (%)
func (h HistoricalFinaMainData) GetAvgParentNetprofitIncreasingRatioByYear(ctx context.Context, year int) float64 {
	data := h.FilterByReportYear(ctx, year)
	dlen := len(data)
	if dlen == 0 {
		return 0
	}
	sum := 0.0
	for _, d := range data {
		sum += d.Parentnetprofittz
	}

	return sum / float64(dlen)
}

// RespFinaMainData 接口返回 json 结构
type RespFinaMainData struct {
	Version string `json:"version"`
	Result  struct {
		Pages int                    `json:"pages"`
		Data  HistoricalFinaMainData `json:"data"`
		Count int                    `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// QueryHistoricalFinaMainData 获取财报主要指标，最新的在最前面
func (e EastMoney) QueryHistoricalFinaMainData(ctx context.Context, secuCode string) (HistoricalFinaMainData, error) {
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/get"
	params := map[string]string{
		"filter": fmt.Sprintf(`(SECUCODE="%s")`, strings.ToUpper(secuCode)),
		"client": "APP",
		"source": "HSF10",
		"type":   "RPT_F10_FINANCE_MAINFINADATA",
		"sty":    "APP_F10_MAINFINADATA",
		"st":     "REPORT_DATE",
		"ps":     "100",
		"sr":     "-1",
	}
	logging.Debug(ctx, "EastMoney QueryHistoricalFinaMainData "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespFinaMainData{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryHistoricalFinaMainData "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", secuCode, resp)
	}
	return resp.Result.Data, nil
}

// FinaPublishDate 财报发布时间
type FinaPublishDate struct {
	SecurityCode       string `json:"SECURITY_CODE"`
	SecurityNameAbbr   string `json:"SECURITY_NAME_ABBR"`
	AppointPublishDate string `json:"APPOINT_PUBLISH_DATE"`
	ReportDate         string `json:"REPORT_DATE"`
	ActualPublishDate  string `json:"ACTUAL_PUBLISH_DATE"`
	ReportTypeName     string `json:"REPORT_TYPE_NAME"`
	IsPublish          string `json:"IS_PUBLISH"`
}

// FinaPublishDateList 历史发布时间
type FinaPublishDateList []FinaPublishDate

// RespFinaPublishDate 财报披露日期接口返回结构
type RespFinaPublishDate struct {
	Version string `json:"version"`
	Result  struct {
		Pages int                 `json:"pages"`
		Data  FinaPublishDateList `json:"data"`
		Count int                 `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// QueryFinaPublishDateList 查询最新财报披露日期
func (e EastMoney) QueryFinaPublishDateList(ctx context.Context, securityCode string) (FinaPublishDateList, error) {
	apiurl := "https://datacenter.eastmoney.com/api/data/get"
	params := map[string]string{
		"filter": fmt.Sprintf(`(SECURITY_CODE="%s")`, strings.ToUpper(securityCode)),
		"client": "APP",
		"source": "DataCenter",
		"type":   "RPT_PUBLIC_BS_APPOIN",
		"sty":    "SECURITY_CODE,SECURITY_NAME_ABBR,APPOINT_PUBLISH_DATE,REPORT_DATE,ACTUAL_PUBLISH_DATE,REPORT_TYPE_NAME,IS_PUBLISH",
		"st":     "SECURITY_CODE,EITIME",
		"ps":     "20",
		"p":      "1",
		"sr":     "-1,-1",
	}
	logging.Debug(ctx, "EastMoney QueryFinaPublishDate "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespFinaPublishDate{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFinaPublishDate "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	if resp.Code != 0 {
		return nil, fmt.Errorf("%s %#v", securityCode, resp)
	}
	return resp.Result.Data, nil
}
