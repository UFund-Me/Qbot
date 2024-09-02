// 股票对象封装

package models

import (
	"context"
	"sort"
	"sync"
	"time"

	"github.com/axiaoxin-com/investool/datacenter"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/investool/datacenter/eniu"
	"github.com/axiaoxin-com/investool/datacenter/zszx"
	"github.com/axiaoxin-com/logging"
)

// Stock 接口返回的股票信息结构
type Stock struct {
	// 东方财富接口返回的基本信息
	BaseInfo eastmoney.StockInfo `json:"base_info"`
	// 历史财报信息
	HistoricalFinaMainData eastmoney.HistoricalFinaMainData `json:"historical_fina_main_data"`
	// 市盈率、市净率、市销率、市现率估值
	ValuationMap map[string]string `json:"valuation_map"`
	// 历史市盈率
	HistoricalPEList eastmoney.HistoricalPEList `json:"historical_pe_list"`
	// 合理价格（年报）：历史市盈率中位数 * (去年EPS * (1 + 今年各期财报的平均营收增长比))
	RightPrice float64 `json:"right_price"`
	// 合理价差（%）
	PriceSpace float64 `json:"price_space"`
	// 按前年年报算去年的合理价格：历史市盈率中位数 * (前年EPS * (1 + 去年各期财报的平均营收增长比))
	LastYearRightPrice float64 `json:"last_year_right_price"`
	// 历史股价
	HistoricalPrice eniu.RespHistoricalStockPrice `json:"historical_price"`
	// 历史波动率
	HistoricalVolatility float64 `json:"historical_volatility"`
	// 公司资料
	CompanyProfile eastmoney.CompanyProfile `json:"company_profile"`
	// 预约财报披露日期
	FinaAppointPublishDate string `json:"fina_appoint_publish_date"`
	// 实际财报披露日期
	FinaActualPublishDate string `json:"fina_actual_publish_date"`
	// 财报披露日期
	FinaReportDate string `json:"fina_report_date"`
	// 机构评级
	OrgRatingList eastmoney.OrgRatingList `json:"org_rating_list"`
	// 盈利预测
	ProfitPredictList eastmoney.ProfitPredictList `json:"profit_predict_list"`
	// 价值评估
	JZPG eastmoney.JZPG `json:"jzpg"`
	// PEG=PE/净利润复合增长率
	PEG float64 `json:"peg"`
	// 历史利润表
	HistoricalGincomeList eastmoney.GincomeDataList `json:"historical_gincome_list"`
	// 本业营收比=营业利润/(营业利润+营业外收入)
	BYYSRatio float64 `json:"byys_ratio"`
	// 最新财报审计意见
	FinaReportOpinion string `json:"fina_report_opinion"`
	// 历史现金流量表
	HistoricalCashflowList eastmoney.CashflowDataList `json:"historical_cashdlow_list"`
	// 最新经营活动产生的现金流量净额
	NetcashOperate float64 `json:"netcash_operate"`
	// 最新投资活动产生的现金流量净额
	NetcashInvest float64 `json:"netcash_invest"`
	// 最新筹资活动产生的现金流量净额
	NetcashFinance float64 `json:"netcash_finance"`
	// 自由现金流
	NetcashFree float64 `json:"netcash_free"`
	// 十大流通股东
	FreeHoldersTop10 eastmoney.FreeHolderList `json:"free_holders_top_10"`
	// 主力资金净流入
	MainMoneyNetInflows zszx.NetInflowList `json:"main_money_net_inflows"`
}

// GetPrice 返回股价，没开盘时可能是字符串“-”，此时返回最近历史股价，无历史价则返回 -1
func (s Stock) GetPrice() float64 {
	p, ok := s.BaseInfo.NewPrice.(float64)
	if ok {
		return p
	}
	if len(s.HistoricalPrice.Price) == 0 {
		return -1.0
	}
	return s.HistoricalPrice.Price[len(s.HistoricalPrice.Price)-1]
}

// GetOrgType 获取机构类型
func (s Stock) GetOrgType() string {
	if len(s.HistoricalFinaMainData) == 0 {
		return ""
	}
	return s.HistoricalFinaMainData[0].OrgType
}

// StockList 股票列表
type StockList []Stock

// SortByROE 股票列表按 ROE 排序
func (s StockList) SortByROE() {
	sort.Slice(s, func(i, j int) bool {
		return s[i].BaseInfo.RoeWeight > s[j].BaseInfo.RoeWeight
	})
}

// SortByPriceSpace 股票列表按合理价差排序
func (s StockList) SortByPriceSpace() {
	sort.Slice(s, func(i, j int) bool {
		return s[i].PriceSpace > s[j].PriceSpace
	})
}

// NewStock 创建 Stock 对象
func NewStock(ctx context.Context, baseInfo eastmoney.StockInfo) (Stock, error) {
	s := Stock{
		BaseInfo: baseInfo,
	}

	// PEG
	s.PEG = s.BaseInfo.PE / s.BaseInfo.NetprofitGrowthrate3Y
	price := s.GetPrice()

	var wg sync.WaitGroup
	// 获取财报
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		hf, err := datacenter.EastMoney.QueryHistoricalFinaMainData(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryHistoricalFinaMainData err:"+err.Error())
			return
		}
		if len(hf) == 0 {
			logging.Error(ctx, "HistoricalFinaMainData is empty")
			return
		}
		s.HistoricalFinaMainData = hf

		// 历史市盈率 && 合理价格
		peList, err := datacenter.EastMoney.QueryHistoricalPEList(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryHistoricalPEList err:"+err.Error())
			return
		}
		s.HistoricalPEList = peList

		// 合理价格判断
		// 去年年报
		lastYearReport := s.HistoricalFinaMainData.GetReport(ctx, time.Now().Year()-1, eastmoney.FinaReportTypeYear)
		beforeLastYearReport := s.HistoricalFinaMainData.GetReport(ctx, time.Now().Year()-2, eastmoney.FinaReportTypeYear)
		thisYear := time.Now().Year()
		thisYearAvgRevIncrRatio := s.HistoricalFinaMainData.GetAvgRevenueIncreasingRatioByYear(ctx, thisYear)
		lastYearAvgRevIncrRatio := s.HistoricalFinaMainData.GetAvgRevenueIncreasingRatioByYear(ctx, thisYear-1)
		// nil fix: 新的一年刚开始时，上一年的年报还没披露，年份数据全部-1，保证有数据返回
		if lastYearReport == nil {
			logging.Debug(ctx, "NewStock get last year report nil, use before last year report")
			lastYearReport = beforeLastYearReport
			beforeLastYearReport = s.HistoricalFinaMainData.GetReport(ctx, time.Now().Year()-3, eastmoney.FinaReportTypeYear)
			thisYearAvgRevIncrRatio = s.HistoricalFinaMainData.GetAvgRevenueIncreasingRatioByYear(ctx, thisYear-1)
			lastYearAvgRevIncrRatio = s.HistoricalFinaMainData.GetAvgRevenueIncreasingRatioByYear(ctx, thisYear-2)
		}
		// pe 中位数
		peMidVal, err := peList.GetMidValue(ctx)
		if err != nil {
			logging.Error(ctx, "NewStock GetMidValue err:"+err.Error())
			return
		}
		s.RightPrice = peMidVal * (lastYearReport.Epsjb * (1 + thisYearAvgRevIncrRatio/100.0))
		s.PriceSpace = (s.RightPrice - price) / price * 100
		s.LastYearRightPrice = peMidVal * (beforeLastYearReport.Epsjb * (1 + lastYearAvgRevIncrRatio/100.0))
	}(ctx, &s)

	// 获取综合估值
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		valMap, err := datacenter.EastMoney.QueryValuationStatus(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryValuationStatus err:"+err.Error())
			return
		}
		s.ValuationMap = valMap
	}(ctx, &s)

	// 历史股价 && 波动率
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		hisPrice, err := datacenter.Eniu.QueryHistoricalStockPrice(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryHistoricalStockPrice err:"+err.Error())
			return
		}
		s.HistoricalPrice = hisPrice

		// 历史波动率
		hv, err := hisPrice.HistoricalVolatility(ctx, "YEAR")
		if err != nil {
			logging.Error(ctx, "NewStock HistoricalVolatility err:"+err.Error())
			return
		}
		s.HistoricalVolatility = hv
	}(ctx, &s)

	// 公司资料
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		cp, err := datacenter.EastMoney.QueryCompanyProfile(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryCompanyProfile err:"+err.Error())
			return
		}
		s.CompanyProfile = cp
	}(ctx, &s)

	// 最新财报预约披露时间
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		finaPubDateList, err := datacenter.EastMoney.QueryFinaPublishDateList(ctx, s.BaseInfo.SecurityCode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryFinaPublishDateList err:"+err.Error())
			return
		}
		if len(finaPubDateList) > 0 {
			s.FinaAppointPublishDate = finaPubDateList[0].AppointPublishDate
			s.FinaActualPublishDate = finaPubDateList[0].ActualPublishDate
			s.FinaReportDate = finaPubDateList[0].ReportDate
		}
	}(ctx, &s)

	// 机构评级统计
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		orgRatings, err := datacenter.EastMoney.QueryOrgRating(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Debug(ctx, "NewStock QueryOrgRating err:"+err.Error())
			return
		}
		s.OrgRatingList = orgRatings
	}(ctx, &s)

	// 盈利预测
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		pps, err := datacenter.EastMoney.QueryProfitPredict(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Debug(ctx, "NewStock QueryProfitPredict err:"+err.Error())
			return
		}
		s.ProfitPredictList = pps
	}(ctx, &s)

	// 价值评估
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		jzpg, err := datacenter.EastMoney.QueryJiaZhiPingGu(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Debug(ctx, "NewStock QueryJiaZhiPingGu err:"+err.Error())
			return
		}
		s.JZPG = jzpg
	}(ctx, &s)

	// 利润表数据
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		gincomeList, err := datacenter.EastMoney.QueryFinaGincomeData(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryFinaGincomeData err:"+err.Error())
			return
		}
		s.HistoricalGincomeList = gincomeList
		if len(s.HistoricalGincomeList) > 0 {
			// 本业营收比
			gincome := s.HistoricalGincomeList[0]
			s.BYYSRatio = gincome.OperateProfit / (gincome.OperateProfit + gincome.NonbusinessIncome)
			// 审计意见
			s.FinaReportOpinion = gincome.OpinionType
		}
	}(ctx, &s)

	// 现金流量表数据
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		cashflow, err := datacenter.EastMoney.QueryFinaCashflowData(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryFinaCashflowData err:"+err.Error())
			return
		}
		s.HistoricalCashflowList = cashflow
		if len(s.HistoricalCashflowList) > 0 {
			cf := s.HistoricalCashflowList[0]
			s.NetcashOperate = cf.NetcashOperate
			s.NetcashInvest = cf.NetcashInvest
			s.NetcashFinance = cf.NetcashFinance
			if cf.NetcashInvest < 0 {
				s.NetcashFree = s.NetcashOperate + s.NetcashInvest
			} else {
				s.NetcashFree = s.NetcashOperate - s.NetcashInvest
			}
		}
	}(ctx, &s)

	// 获取前10大流通股东
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		holders, err := datacenter.EastMoney.QueryFreeHolders(ctx, s.BaseInfo.Secucode)
		if err != nil {
			logging.Error(ctx, "NewStock QueryFreeHolders err:"+err.Error())
			return
		}
		s.FreeHoldersTop10 = holders
	}(ctx, &s)

	// 获取最近60日的主力资金净流入
	wg.Add(1)
	go func(ctx context.Context, s *Stock) {
		defer wg.Done()
		now := time.Now()
		end := now.Format("2006-01-02")
		d, _ := time.ParseDuration("-1440h")
		start := now.Add(d).Format("2006-01-02")
		inflows, err := datacenter.Zszx.QueryMainMoneyNetInflows(ctx, s.BaseInfo.Secucode, start, end)
		if err != nil {
			logging.Error(ctx, "NewStock QueryMainMoneyNetInflows err:"+err.Error())
			return
		}
		s.MainMoneyNetInflows = inflows
	}(ctx, &s)

	wg.Wait()

	return s, nil
}
