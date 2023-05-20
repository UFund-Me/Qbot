// 获取公司简介资料

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

// RespJBZL 基本资料接口返回结构
type RespJBZL struct {
	Result struct {
		Jibenziliao struct {
			Secucode          string `json:"SecurityCode"`
			Companycode       string `json:"CompanyCode"`
			Companyname       string `json:"CompanyName"`
			Previousname      string `json:"PreviousName"`
			Provice           string `json:"Provice"`
			Industry          string `json:"Industry"`
			Block             string `json:"Block"`
			Chairman          string `json:"Chairman"`
			Website           string `json:"Website"`
			Registeredaddress string `json:"RegisteredAddress"`
			Officeaddress     string `json:"OfficeAddress"`
			Comprofile        string `json:"CompRofile"`
			Mainbusiness      string `json:"MainBusiness"`
			Securitycodea     string `json:"SecurityCodeA"`
			Securitynamea     string `json:"SecurityNameA"`
			Securitycodeb     string `json:"SecurityCodeB"`
			Securitynameb     string `json:"SecurityNameB"`
			Securitycodeh     string `json:"SecurityCodeH"`
			Securitynameh     string `json:"SecurityNameH"`
			Representative    string `json:"Representative"`
			Generalmanager    string `json:"GeneralManager"`
			Secretaries       string `json:"Secretaries"`
			Founddate         string `json:"FoundDate"`
			Registeredcapital string `json:"RegisteredCapital"`
			Currency          string `json:"Currency"`
			Employees         string `json:"Employees"`
			Managers          string `json:"Managers"`
			Phone             string `json:"Phone"`
			Email             string `json:"Email"`
			Securitycodetype  string `json:"SecurityCodeType"`
			Codetype          string `json:"CodeType"`
			Isinnovation      int    `json:"IsInnovation"`
		} `json:"JiBenZiLiao"`
	} `json:"Result"`
	Status    int    `json:"Status"`
	Message   string `json:"Message"`
	Otherinfo struct {
	} `json:"OtherInfo"`
}

// RespCPBD 操盘必读接口返回结构
type RespCPBD struct {
	Result struct {
		Ticaixiangqinglist []struct {
			Secucode           string `json:"SecurityCode"`
			Keyword            string `json:"KeyWord"`
			Mainpoint          string `json:"MainPoint"`
			Mainpointcon       string `json:"MainPointCon"`
			Classification     string `json:"Classification"`
			Classificationname string `json:"ClassificationName"`
			Ispoint            string `json:"IsPoint"`
		} `json:"TiCaiXiangQingList"`
		Gubengudong struct {
			Reportdate                              string `json:"ReportDate"`
			Securitycode                            string `json:"SecurityCode"`
			Totalequity                             string `json:"TotalEquity"`
			Totalequitypercent                      string `json:"TotalEquityPercent"`
			Ashares                                 string `json:"Ashares"`
			Asharespercent                          string `json:"ASharesPercent"`
			Asharespercentchart                     string `json:"ASharesPercentChart"`
			Restrictedcirculationshares             string `json:"RestrictedCirculationShares"`
			Restrictedcirculationsharespercent      string `json:"RestrictedCirculationSharesPercent"`
			Restrictedcirculationsharespercentchart string `json:"RestrictedCirculationSharesPercentChart"`
		} `json:"GuBenGuDong"`
		Gudongrenshuunit string `json:"GuDongRenShuUnit"`
		Gudongrenshulist []struct {
			Secucode                string `json:"SecurityCode"`
			Changedate              string `json:"ChangeDate"`
			Totalsh                 string `json:"TotalSh"`
			Totalshchart            string `json:"TotalShChart"`
			Changewithlasttermsh    string `json:"ChangeWithLastTermSh"`
			Avgshare                string `json:"AvgShare"`
			Changewithlasttermshare string `json:"ChangeWithLastTermShare"`
			Stockprice              string `json:"StockPrice"`
			Stockconvergencerate    string `json:"StockConvergenceRate"`
			Sumlishold              string `json:"SumLishold"`
			Sumcirlishold           string `json:"SumCirLishold"`
		} `json:"GuDongRenShuList"`
		Gudongtongji struct {
			Secucode                  string `json:"SecurityCode"`
			Reportdate                string `json:"ReportDate"`
			Actualcontroller          string `json:"ActualController"`
			Actualcontrollerrate      string `json:"ActualControllerRate"`
			Shareholdercontroller     string `json:"ShareholderController"`
			Shareholdercontrollerrate string `json:"ShareholderControllerRate"`
			Shareholder               string `json:"ShareHolder"`
			Shareholderrate           string `json:"ShareHolderRate"`
			Cirshareholder            string `json:"CirShareHolder"`
			Cirshareholderrate        string `json:"CirShareHolderRate"`
			Orgholdernum              string `json:"OrgHolderNum"`
			Orgholderrate             string `json:"OrgHolderRate"`
			Orgholdernumpre           string `json:"OrgHolderNumPre"`
			Orgholderratepre          string `json:"OrgHolderRatePre"`
		} `json:"GuDongTongJi"`
		Zhuyinggouchenglist []struct {
			Secucode             string `json:"SecurityCode"`
			Reporttype           string `json:"ReportType"`
			Reportdate           string `json:"ReportDate"`
			Mainform             string `json:"MainForm"`
			Mainincome           string `json:"MainIncome"`
			Mainincomeratio      string `json:"MainIncomeRatio"`
			Mainincomeratiochart string `json:"MainIncomeRatioChart"`
			Flag                 string `json:"Flag"`
		} `json:"ZhuYingGouChengList"`
		Fenhongsongzhuanlist []struct {
			Secucode       string `json:"SecurityCode"`
			Noticedate     string `json:"NoticeDate"`
			Assigndscrpt   string `json:"AssignDscrpt"`
			Exdividenddate string `json:"ExDividendDate"`
			Rightregdate   string `json:"RightRegDate"`
		} `json:"FenHongSongZhuanList"`
		Jinglirununit    string `json:"JingliRunUnit"`
		Yingyeshouruunit string `json:"YingYeShouRuUnit"`
		Danjicaiwulist   []struct {
			Secucode         string `json:"SecurityCode"`
			Reportdate       string `json:"ReportDate"`
			Netprofit        string `json:"NetProfit"`
			Netprofitchart   string `json:"NetProfitChart"`
			Eps              string `json:"EPS"`
			Epschart         string `json:"EPSChart"`
			Totalincome      string `json:"TotalIncome"`
			Totalincomechart string `json:"TotalIncomeChart"`
			Year             string `json:"Year"`
		} `json:"DanJiCaiWuList"`
		Guquanzhiyatujielist []struct {
			Tradedate     string `json:"TradeDate"`
			Amtshareratio string `json:"AmtShareRatio"`
		} `json:"GuQuanZhiYaTuJieList"`
		Guquanzhiyatongjilist interface{} `json:"GuQuanZhiYaTongJiList"`
		Shangyuqingkuang      struct {
			Tujiedatalist []struct {
				Baogaoqi          string      `json:"BaoGaoQi"`
				Shangyuzhi        string      `json:"ShangYuZhi"`
				Shangyuzhitext    interface{} `json:"ShangYuZhiText"`
				Shangyuzhiunit    interface{} `json:"ShangYuZhiUnit"`
				Jingzichanjiazong interface{} `json:"JingZiChanJiaZong"`
				Shangyujingzichan string      `json:"ShangYuJingZiChan"`
			} `json:"TuJieDataList"`
			Data struct {
				Code                    string      `json:"Code"`
				Baogaoqi                string      `json:"BaoGaoQi"`
				Baogaoqileixing         string      `json:"BaoGaoQiLeiXing"`
				Shangyu                 string      `json:"ShangYu"`
				Shangyutongbi           string      `json:"ShangYuTongBi"`
				Shangyujingzichan       string      `json:"ShangYuJingZiChan"`
				Shangyujingzichantongbi string      `json:"ShangYuJingZiChanTongBi"`
				Guimujinglirun          string      `json:"GuiMuJingLiRun"`
				Guimujingliruntongbi    string      `json:"GuiMuJingLiRunTongBi"`
				Shifouxianshi           interface{} `json:"ShiFouXianShi"`
			} `json:"Data"`
		} `json:"ShangYuQingKuang"`
		Yanfatourulist []interface{} `json:"YanFaTouRuList"`
	} `json:"Result"`
	Status    int         `json:"Status"`
	Message   interface{} `json:"Message"`
	Otherinfo struct {
	} `json:"OtherInfo"`
}

// MainForm 主营构成
type MainForm struct {
	// 分类类型： 1 按行业分类 2 按地区分类 3 按产品分类
	Type string `json:"type"`
	// 名称
	MainForm string `json:"main_form"`
	// 占比
	MainIncomeRatio string `json:"main_income_ratio"`
	// 金额
	MainIncome string `json:"main_income"`
	// 精确数字
	MainIncomeRatioChart string `json:"main_income_ratio_chart"`
}

// CompanyProfile 公司简介资料
type CompanyProfile struct {
	// 股票代码
	Secucode string
	// 公司名称
	Name string
	// 所属行业
	Industry string `json:"industry"`
	// 所属概念
	Concept string `json:"concept"`
	// 简介
	Profile string `json:"profile"`
	// 主营业务
	MainBusiness string `json:"main_business"`
	// 题材关键词
	Keywords []string `json:"keywords"`
	// 主营构成
	MainForms []MainForm `json:"main_forms"`
}

// MainFormsString 主营构成字符串
func (c CompanyProfile) MainFormsString() string {
	group := map[string][]MainForm{}
	for _, m := range c.MainForms {
		group[m.Type] = append(group[m.Type], m)
	}
	s := []string{"按行业:"}
	if len(group["1"]) > 0 {
		for _, m := range group["1"] {
			s = append(s, fmt.Sprintf("    %s: %s", m.MainForm, m.MainIncomeRatio))
		}
	} else {
		s = append(s, "暂无数据")
	}

	s = append(s, "按产品:")
	if len(group["3"]) > 0 {
		for _, m := range group["3"] {
			s = append(s, fmt.Sprintf("    %s: %s", m.MainForm, m.MainIncomeRatio))
		}
	} else {
		s = append(s, "暂无数据")
	}

	s = append(s, "按地区:")
	if len(group["2"]) > 0 {
		for _, m := range group["2"] {
			s = append(s, fmt.Sprintf("    %s: %s", m.MainForm, m.MainIncomeRatio))
		}
	} else {
		s = append(s, "暂无数据")
	}

	return strings.Join(s, "\n")
}

// ProfileString 公司信息
func (c CompanyProfile) ProfileString() string {
	s := []string{"公司简介:"}
	s = append(s, c.Profile)
	s = append(s, "主营业务:")
	s = append(s, "    "+c.MainBusiness)
	s = append(s, "所属概念:")
	s = append(s, "    "+c.Concept)

	return strings.Join(s, "\n")
}

// KeywordsString 关键词字符串
func (c CompanyProfile) KeywordsString() string {
	return strings.Join(c.Keywords, ";")
}

// QueryCompanyProfile 获取公司信息
func (e EastMoney) QueryCompanyProfile(ctx context.Context, secuCode string) (CompanyProfile, error) {
	profile := CompanyProfile{}
	fc := e.GetFC(secuCode)

	// 基本资料
	apiurl := "https://emh5.eastmoney.com/api/GongSiGaiKuang/GetJiBenZiLiao"
	reqData := map[string]interface{}{
		"fc": fc,
	}
	logging.Debug(ctx, "EastMoney QueryCompanyProfile "+apiurl+" begin", zap.Any("reqData", reqData))
	beginTime := time.Now()
	req, err := goutils.NewHTTPJSONReq(ctx, apiurl, reqData)
	if err != nil {
		return profile, err
	}
	resp := RespJBZL{}
	err = goutils.HTTPPOST(ctx, e.HTTPClient, req, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryCompanyProfile "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return profile, err
	}
	if resp.Status != 0 {
		return profile, fmt.Errorf("%s %#v", secuCode, resp.Message)
	}
	profile.Secucode = resp.Result.Jibenziliao.Secucode
	profile.Name = resp.Result.Jibenziliao.Companyname
	profile.Industry = resp.Result.Jibenziliao.Industry
	profile.Concept = resp.Result.Jibenziliao.Block
	profile.Profile = resp.Result.Jibenziliao.Comprofile
	profile.MainBusiness = resp.Result.Jibenziliao.Mainbusiness

	// 操盘必读
	apiurl = "https://emh5.eastmoney.com/api/CaoPanBiDu/GetCaoPanBiDuPart2Get"
	params := map[string]string{
		"fc": fc,
	}
	logging.Debug(ctx, "EastMoney QueryCompanyProfile "+apiurl+" begin", zap.Any("params", params))
	beginTime = time.Now()
	apiurl, err = goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return profile, err
	}
	resp1 := RespCPBD{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp1)
	latency = time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryCompanyProfile "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp1),
	)
	if err != nil {
		return profile, err
	}
	if resp1.Status != 0 {
		return profile, fmt.Errorf("%s %#v", secuCode, resp1.Message)
	}
	for _, i := range resp1.Result.Ticaixiangqinglist {
		profile.Keywords = append(profile.Keywords, i.Keyword)
	}
	for _, i := range resp1.Result.Zhuyinggouchenglist {
		m := MainForm{
			Type:                 i.Reporttype,
			MainForm:             i.Mainform,
			MainIncome:           i.Mainincome,
			MainIncomeRatio:      i.Mainincomeratio,
			MainIncomeRatioChart: i.Mainincomeratiochart,
		}
		profile.MainForms = append(profile.MainForms, m)
	}
	return profile, nil
}

// GetFC 生成 fc 请求参数
func (e EastMoney) GetFC(secuCode string) string {
	secuCode = strings.ToUpper(secuCode)
	fc := ""
	if strings.HasSuffix(secuCode, ".SH") {
		fc = strings.Replace(secuCode, ".SH", "01", -1)
	} else if strings.HasSuffix(secuCode, ".SZ") {
		fc = strings.Replace(secuCode, ".SZ", "02", -1)
	}
	return fc
}
