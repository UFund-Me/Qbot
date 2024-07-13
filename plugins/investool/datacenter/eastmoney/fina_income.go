// 获取财务分析利润表数据

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

// GincomeData 财务分析利润表数据
type GincomeData struct {
	Secucode                     string         `json:"SECUCODE"`
	SecurityCode                 string         `json:"SECURITY_CODE"`
	SecurityNameAbbr             string         `json:"SECURITY_NAME_ABBR"`
	OrgCode                      string         `json:"ORG_CODE"`
	OrgType                      string         `json:"ORG_TYPE"`
	ReportDate                   string         `json:"REPORT_DATE"`
	ReportType                   FinaReportType `json:"REPORT_TYPE"`
	ReportDateName               string         `json:"REPORT_DATE_NAME"`
	SecurityTypeCode             string         `json:"SECURITY_TYPE_CODE"`
	NoticeDate                   string         `json:"NOTICE_DATE"`
	UpdateDate                   string         `json:"UPDATE_DATE"`
	Currency                     string         `json:"CURRENCY"`
	TotalOperateIncome           float64        `json:"TOTAL_OPERATE_INCOME"`
	TotalOperateIncomeYoy        float64        `json:"TOTAL_OPERATE_INCOME_YOY"`
	OperateIncome                float64        `json:"OPERATE_INCOME"`
	OperateIncomeYoy             float64        `json:"OPERATE_INCOME_YOY"`
	InterestIncome               interface{}    `json:"INTEREST_INCOME"`
	InterestIncomeYoy            interface{}    `json:"INTEREST_INCOME_YOY"`
	EarnedPremium                interface{}    `json:"EARNED_PREMIUM"`
	EarnedPremiumYoy             interface{}    `json:"EARNED_PREMIUM_YOY"`
	FeeCommissionIncome          interface{}    `json:"FEE_COMMISSION_INCOME"`
	FeeCommissionIncomeYoy       interface{}    `json:"FEE_COMMISSION_INCOME_YOY"`
	OtherBusinessIncome          interface{}    `json:"OTHER_BUSINESS_INCOME"`
	OtherBusinessIncomeYoy       interface{}    `json:"OTHER_BUSINESS_INCOME_YOY"`
	ToiOther                     interface{}    `json:"TOI_OTHER"`
	ToiOtherYoy                  interface{}    `json:"TOI_OTHER_YOY"`
	TotalOperateCost             float64        `json:"TOTAL_OPERATE_COST"`
	TotalOperateCostYoy          float64        `json:"TOTAL_OPERATE_COST_YOY"`
	OperateCost                  float64        `json:"OPERATE_COST"`
	OperateCostYoy               float64        `json:"OPERATE_COST_YOY"`
	InterestExpense              interface{}    `json:"INTEREST_EXPENSE"`
	InterestExpenseYoy           interface{}    `json:"INTEREST_EXPENSE_YOY"`
	FeeCommissionExpense         interface{}    `json:"FEE_COMMISSION_EXPENSE"`
	FeeCommissionExpenseYoy      interface{}    `json:"FEE_COMMISSION_EXPENSE_YOY"`
	ResearchExpense              float64        `json:"RESEARCH_EXPENSE"`
	ResearchExpenseYoy           float64        `json:"RESEARCH_EXPENSE_YOY"`
	SurrenderValue               interface{}    `json:"SURRENDER_VALUE"`
	SurrenderValueYoy            interface{}    `json:"SURRENDER_VALUE_YOY"`
	NetCompensateExpense         interface{}    `json:"NET_COMPENSATE_EXPENSE"`
	NetCompensateExpenseYoy      interface{}    `json:"NET_COMPENSATE_EXPENSE_YOY"`
	NetContractReserve           interface{}    `json:"NET_CONTRACT_RESERVE"`
	NetContractReserveYoy        interface{}    `json:"NET_CONTRACT_RESERVE_YOY"`
	PolicyBonusExpense           interface{}    `json:"POLICY_BONUS_EXPENSE"`
	PolicyBonusExpenseYoy        interface{}    `json:"POLICY_BONUS_EXPENSE_YOY"`
	ReinsureExpense              interface{}    `json:"REINSURE_EXPENSE"`
	ReinsureExpenseYoy           interface{}    `json:"REINSURE_EXPENSE_YOY"`
	OtherBusinessCost            interface{}    `json:"OTHER_BUSINESS_COST"`
	OtherBusinessCostYoy         interface{}    `json:"OTHER_BUSINESS_COST_YOY"`
	OperateTaxAdd                float64        `json:"OPERATE_TAX_ADD"`
	OperateTaxAddYoy             float64        `json:"OPERATE_TAX_ADD_YOY"`
	SaleExpense                  float64        `json:"SALE_EXPENSE"`
	SaleExpenseYoy               float64        `json:"SALE_EXPENSE_YOY"`
	ManageExpense                float64        `json:"MANAGE_EXPENSE"`
	ManageExpenseYoy             float64        `json:"MANAGE_EXPENSE_YOY"`
	MeResearchExpense            interface{}    `json:"ME_RESEARCH_EXPENSE"`
	MeResearchExpenseYoy         interface{}    `json:"ME_RESEARCH_EXPENSE_YOY"`
	FinanceExpense               float64        `json:"FINANCE_EXPENSE"`
	FinanceExpenseYoy            float64        `json:"FINANCE_EXPENSE_YOY"`
	FeInterestExpense            float64        `json:"FE_INTEREST_EXPENSE"`
	FeInterestExpenseYoy         float64        `json:"FE_INTEREST_EXPENSE_YOY"`
	FeInterestIncome             float64        `json:"FE_INTEREST_INCOME"`
	FeInterestIncomeYoy          float64        `json:"FE_INTEREST_INCOME_YOY"`
	AssetImpairmentLoss          interface{}    `json:"ASSET_IMPAIRMENT_LOSS"`
	AssetImpairmentLossYoy       interface{}    `json:"ASSET_IMPAIRMENT_LOSS_YOY"`
	CreditImpairmentLoss         interface{}    `json:"CREDIT_IMPAIRMENT_LOSS"`
	CreditImpairmentLossYoy      interface{}    `json:"CREDIT_IMPAIRMENT_LOSS_YOY"`
	TocOther                     interface{}    `json:"TOC_OTHER"`
	TocOtherYoy                  interface{}    `json:"TOC_OTHER_YOY"`
	FairvalueChangeIncome        interface{}    `json:"FAIRVALUE_CHANGE_INCOME"`
	FairvalueChangeIncomeYoy     interface{}    `json:"FAIRVALUE_CHANGE_INCOME_YOY"`
	InvestIncome                 interface{}    `json:"INVEST_INCOME"`
	InvestIncomeYoy              interface{}    `json:"INVEST_INCOME_YOY"`
	InvestJointIncome            interface{}    `json:"INVEST_JOINT_INCOME"`
	InvestJointIncomeYoy         interface{}    `json:"INVEST_JOINT_INCOME_YOY"`
	NetExposureIncome            interface{}    `json:"NET_EXPOSURE_INCOME"`
	NetExposureIncomeYoy         interface{}    `json:"NET_EXPOSURE_INCOME_YOY"`
	ExchangeIncome               interface{}    `json:"EXCHANGE_INCOME"`
	ExchangeIncomeYoy            interface{}    `json:"EXCHANGE_INCOME_YOY"`
	AssetDisposalIncome          float64        `json:"ASSET_DISPOSAL_INCOME"`
	AssetDisposalIncomeYoy       interface{}    `json:"ASSET_DISPOSAL_INCOME_YOY"`
	AssetImpairmentIncome        float64        `json:"ASSET_IMPAIRMENT_INCOME"`
	AssetImpairmentIncomeYoy     float64        `json:"ASSET_IMPAIRMENT_INCOME_YOY"`
	CreditImpairmentIncome       float64        `json:"CREDIT_IMPAIRMENT_INCOME"`
	CreditImpairmentIncomeYoy    interface{}    `json:"CREDIT_IMPAIRMENT_INCOME_YOY"`
	OtherIncome                  float64        `json:"OTHER_INCOME"`
	OtherIncomeYoy               interface{}    `json:"OTHER_INCOME_YOY"`
	OperateProfitOther           interface{}    `json:"OPERATE_PROFIT_OTHER"`
	OperateProfitOtherYoy        interface{}    `json:"OPERATE_PROFIT_OTHER_YOY"`
	OperateProfitBalance         float64        `json:"OPERATE_PROFIT_BALANCE"`
	OperateProfitBalanceYoy      interface{}    `json:"OPERATE_PROFIT_BALANCE_YOY"`
	OperateProfit                float64        `json:"OPERATE_PROFIT"`
	OperateProfitYoy             float64        `json:"OPERATE_PROFIT_YOY"`
	NonbusinessIncome            float64        `json:"NONBUSINESS_INCOME"`
	NonbusinessIncomeYoy         float64        `json:"NONBUSINESS_INCOME_YOY"`
	NoncurrentDisposalIncome     interface{}    `json:"NONCURRENT_DISPOSAL_INCOME"`
	NoncurrentDisposalIncomeYoy  interface{}    `json:"NONCURRENT_DISPOSAL_INCOME_YOY"`
	NonbusinessExpense           float64        `json:"NONBUSINESS_EXPENSE"`
	NonbusinessExpenseYoy        float64        `json:"NONBUSINESS_EXPENSE_YOY"`
	NoncurrentDisposalLoss       interface{}    `json:"NONCURRENT_DISPOSAL_LOSS"`
	NoncurrentDisposalLossYoy    interface{}    `json:"NONCURRENT_DISPOSAL_LOSS_YOY"`
	EffectTpOther                interface{}    `json:"EFFECT_TP_OTHER"`
	EffectTpOtherYoy             interface{}    `json:"EFFECT_TP_OTHER_YOY"`
	TotalProfitBalance           float64        `json:"TOTAL_PROFIT_BALANCE"`
	TotalProfitBalanceYoy        interface{}    `json:"TOTAL_PROFIT_BALANCE_YOY"`
	TotalProfit                  float64        `json:"TOTAL_PROFIT"`
	TotalProfitYoy               float64        `json:"TOTAL_PROFIT_YOY"`
	IncomeTax                    float64        `json:"INCOME_TAX"`
	IncomeTaxYoy                 float64        `json:"INCOME_TAX_YOY"`
	EffectNetprofitOther         interface{}    `json:"EFFECT_NETPROFIT_OTHER"`
	EffectNetprofitOtherYoy      interface{}    `json:"EFFECT_NETPROFIT_OTHER_YOY"`
	EffectNetprofitBalance       interface{}    `json:"EFFECT_NETPROFIT_BALANCE"`
	EffectNetprofitBalanceYoy    interface{}    `json:"EFFECT_NETPROFIT_BALANCE_YOY"`
	UnconfirmInvestLoss          interface{}    `json:"UNCONFIRM_INVEST_LOSS"`
	UnconfirmInvestLossYoy       interface{}    `json:"UNCONFIRM_INVEST_LOSS_YOY"`
	Netprofit                    float64        `json:"NETPROFIT"`
	NetprofitYoy                 float64        `json:"NETPROFIT_YOY"`
	PrecombineProfit             interface{}    `json:"PRECOMBINE_PROFIT"`
	PrecombineProfitYoy          interface{}    `json:"PRECOMBINE_PROFIT_YOY"`
	ContinuedNetprofit           float64        `json:"CONTINUED_NETPROFIT"`
	ContinuedNetprofitYoy        float64        `json:"CONTINUED_NETPROFIT_YOY"`
	DiscontinuedNetprofit        interface{}    `json:"DISCONTINUED_NETPROFIT"`
	DiscontinuedNetprofitYoy     interface{}    `json:"DISCONTINUED_NETPROFIT_YOY"`
	ParentNetprofit              float64        `json:"PARENT_NETPROFIT"`
	ParentNetprofitYoy           float64        `json:"PARENT_NETPROFIT_YOY"`
	MinorityInterest             float64        `json:"MINORITY_INTEREST"`
	MinorityInterestYoy          float64        `json:"MINORITY_INTEREST_YOY"`
	DeductParentNetprofit        float64        `json:"DEDUCT_PARENT_NETPROFIT"`
	DeductParentNetprofitYoy     float64        `json:"DEDUCT_PARENT_NETPROFIT_YOY"`
	NetprofitOther               interface{}    `json:"NETPROFIT_OTHER"`
	NetprofitOtherYoy            interface{}    `json:"NETPROFIT_OTHER_YOY"`
	NetprofitBalance             interface{}    `json:"NETPROFIT_BALANCE"`
	NetprofitBalanceYoy          interface{}    `json:"NETPROFIT_BALANCE_YOY"`
	BasicEps                     float64        `json:"BASIC_EPS"`
	BasicEpsYoy                  float64        `json:"BASIC_EPS_YOY"`
	DilutedEps                   float64        `json:"DILUTED_EPS"`
	DilutedEpsYoy                float64        `json:"DILUTED_EPS_YOY"`
	OtherCompreIncome            interface{}    `json:"OTHER_COMPRE_INCOME"`
	OtherCompreIncomeYoy         interface{}    `json:"OTHER_COMPRE_INCOME_YOY"`
	ParentOci                    interface{}    `json:"PARENT_OCI"`
	ParentOciYoy                 interface{}    `json:"PARENT_OCI_YOY"`
	MinorityOci                  interface{}    `json:"MINORITY_OCI"`
	MinorityOciYoy               interface{}    `json:"MINORITY_OCI_YOY"`
	ParentOciOther               interface{}    `json:"PARENT_OCI_OTHER"`
	ParentOciOtherYoy            interface{}    `json:"PARENT_OCI_OTHER_YOY"`
	ParentOciBalance             interface{}    `json:"PARENT_OCI_BALANCE"`
	ParentOciBalanceYoy          interface{}    `json:"PARENT_OCI_BALANCE_YOY"`
	UnableOci                    interface{}    `json:"UNABLE_OCI"`
	UnableOciYoy                 interface{}    `json:"UNABLE_OCI_YOY"`
	CreditriskFairvalueChange    interface{}    `json:"CREDITRISK_FAIRVALUE_CHANGE"`
	CreditriskFairvalueChangeYoy interface{}    `json:"CREDITRISK_FAIRVALUE_CHANGE_YOY"`
	OtherrightFairvalueChange    interface{}    `json:"OTHERRIGHT_FAIRVALUE_CHANGE"`
	OtherrightFairvalueChangeYoy interface{}    `json:"OTHERRIGHT_FAIRVALUE_CHANGE_YOY"`
	SetupProfitChange            interface{}    `json:"SETUP_PROFIT_CHANGE"`
	SetupProfitChangeYoy         interface{}    `json:"SETUP_PROFIT_CHANGE_YOY"`
	RightlawUnableOci            interface{}    `json:"RIGHTLAW_UNABLE_OCI"`
	RightlawUnableOciYoy         interface{}    `json:"RIGHTLAW_UNABLE_OCI_YOY"`
	UnableOciOther               interface{}    `json:"UNABLE_OCI_OTHER"`
	UnableOciOtherYoy            interface{}    `json:"UNABLE_OCI_OTHER_YOY"`
	UnableOciBalance             interface{}    `json:"UNABLE_OCI_BALANCE"`
	UnableOciBalanceYoy          interface{}    `json:"UNABLE_OCI_BALANCE_YOY"`
	AbleOci                      interface{}    `json:"ABLE_OCI"`
	AbleOciYoy                   interface{}    `json:"ABLE_OCI_YOY"`
	RightlawAbleOci              interface{}    `json:"RIGHTLAW_ABLE_OCI"`
	RightlawAbleOciYoy           interface{}    `json:"RIGHTLAW_ABLE_OCI_YOY"`
	AfaFairvalueChange           interface{}    `json:"AFA_FAIRVALUE_CHANGE"`
	AfaFairvalueChangeYoy        interface{}    `json:"AFA_FAIRVALUE_CHANGE_YOY"`
	HmiAfa                       interface{}    `json:"HMI_AFA"`
	HmiAfaYoy                    interface{}    `json:"HMI_AFA_YOY"`
	CashflowHedgeValid           interface{}    `json:"CASHFLOW_HEDGE_VALID"`
	CashflowHedgeValidYoy        interface{}    `json:"CASHFLOW_HEDGE_VALID_YOY"`
	CreditorFairvalueChange      interface{}    `json:"CREDITOR_FAIRVALUE_CHANGE"`
	CreditorFairvalueChangeYoy   interface{}    `json:"CREDITOR_FAIRVALUE_CHANGE_YOY"`
	CreditorImpairmentReserve    interface{}    `json:"CREDITOR_IMPAIRMENT_RESERVE"`
	CreditorImpairmentReserveYoy interface{}    `json:"CREDITOR_IMPAIRMENT_RESERVE_YOY"`
	FinanceOciAmt                interface{}    `json:"FINANCE_OCI_AMT"`
	FinanceOciAmtYoy             interface{}    `json:"FINANCE_OCI_AMT_YOY"`
	ConvertDiff                  interface{}    `json:"CONVERT_DIFF"`
	ConvertDiffYoy               interface{}    `json:"CONVERT_DIFF_YOY"`
	AbleOciOther                 interface{}    `json:"ABLE_OCI_OTHER"`
	AbleOciOtherYoy              interface{}    `json:"ABLE_OCI_OTHER_YOY"`
	AbleOciBalance               interface{}    `json:"ABLE_OCI_BALANCE"`
	AbleOciBalanceYoy            interface{}    `json:"ABLE_OCI_BALANCE_YOY"`
	OciOther                     interface{}    `json:"OCI_OTHER"`
	OciOtherYoy                  interface{}    `json:"OCI_OTHER_YOY"`
	OciBalance                   interface{}    `json:"OCI_BALANCE"`
	OciBalanceYoy                interface{}    `json:"OCI_BALANCE_YOY"`
	TotalCompreIncome            float64        `json:"TOTAL_COMPRE_INCOME"`
	TotalCompreIncomeYoy         float64        `json:"TOTAL_COMPRE_INCOME_YOY"`
	ParentTci                    float64        `json:"PARENT_TCI"`
	ParentTciYoy                 float64        `json:"PARENT_TCI_YOY"`
	MinorityTci                  float64        `json:"MINORITY_TCI"`
	MinorityTciYoy               float64        `json:"MINORITY_TCI_YOY"`
	PrecombineTci                interface{}    `json:"PRECOMBINE_TCI"`
	PrecombineTciYoy             interface{}    `json:"PRECOMBINE_TCI_YOY"`
	EffectTciBalance             interface{}    `json:"EFFECT_TCI_BALANCE"`
	EffectTciBalanceYoy          interface{}    `json:"EFFECT_TCI_BALANCE_YOY"`
	TciOther                     interface{}    `json:"TCI_OTHER"`
	TciOtherYoy                  interface{}    `json:"TCI_OTHER_YOY"`
	TciBalance                   interface{}    `json:"TCI_BALANCE"`
	TciBalanceYoy                interface{}    `json:"TCI_BALANCE_YOY"`
	AcfEndIncome                 interface{}    `json:"ACF_END_INCOME"`
	AcfEndIncomeYoy              interface{}    `json:"ACF_END_INCOME_YOY"`
	OpinionType                  string         `json:"OPINION_TYPE"`
}

// GincomeDataList 利润表历史数据
type GincomeDataList []GincomeData

// RespFinaGincomeData 财务分析利润表接口返回结构
type RespFinaGincomeData struct {
	Version string `json:"version"`
	Result  struct {
		Pages int             `json:"pages"`
		Data  GincomeDataList `json:"data"`
		Count int             `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// QueryFinaGincomeData 获取财务分析利润表数据，最新数据在最前面
func (e EastMoney) QueryFinaGincomeData(ctx context.Context, secuCode string) (GincomeDataList, error) {
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/get"
	params := map[string]string{
		"source": "HSF10",
		"client": "APP",
		"type":   "RPT_F10_FINANCE_GINCOME",
		"sty":    "APP_F10_GINCOME",
		"filter": fmt.Sprintf(`(SECUCODE="%s")`, strings.ToUpper(secuCode)),
		"ps":     "10",
		"sr":     "-1",
		"st":     "REPORT_DATE",
	}
	logging.Debug(ctx, "EastMoney QueryFinaGincomeData "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespFinaGincomeData{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFinaGincomeData "+apiurl+" end",
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
