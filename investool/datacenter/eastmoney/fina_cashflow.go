// 获取财务分析现金流量表数据

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

// CashflowData 现金流量数据
type CashflowData struct {
	Secucode                  string         `json:"SECUCODE"`
	SecurityCode              string         `json:"SECURITY_CODE"`
	SecurityNameAbbr          string         `json:"SECURITY_NAME_ABBR"`
	OrgCode                   string         `json:"ORG_CODE"`
	OrgType                   string         `json:"ORG_TYPE"`
	ReportDate                string         `json:"REPORT_DATE"`
	ReportType                FinaReportType `json:"REPORT_TYPE"`
	ReportDateName            string         `json:"REPORT_DATE_NAME"`
	SecurityTypeCode          string         `json:"SECURITY_TYPE_CODE"`
	NoticeDate                string         `json:"NOTICE_DATE"`
	UpdateDate                string         `json:"UPDATE_DATE"`
	Currency                  string         `json:"CURRENCY"`
	SalesServices             float64        `json:"SALES_SERVICES"`
	DepositInterbankAdd       float64        `json:"DEPOSIT_INTERBANK_ADD"`
	LoanPbcAdd                float64        `json:"LOAN_PBC_ADD"`
	OfiBfAdd                  float64        `json:"OFI_BF_ADD"`
	ReceiveOrigicPremium      float64        `json:"RECEIVE_ORIGIC_PREMIUM"`
	ReceiveReinsureNet        float64        `json:"RECEIVE_REINSURE_NET"`
	InsuredInvestAdd          float64        `json:"INSURED_INVEST_ADD"`
	DisposalTfaAdd            float64        `json:"DISPOSAL_TFA_ADD"`
	ReceiveInterestCommission float64        `json:"RECEIVE_INTEREST_COMMISSION"`
	BorrowFundAdd             float64        `json:"BORROW_FUND_ADD"`
	LoanAdvanceReduce         float64        `json:"LOAN_ADVANCE_REDUCE"`
	RepoBusinessAdd           float64        `json:"REPO_BUSINESS_ADD"`
	ReceiveTaxRefund          float64        `json:"RECEIVE_TAX_REFUND"`
	ReceiveOtherOperate       float64        `json:"RECEIVE_OTHER_OPERATE"`
	OperateInflowOther        float64        `json:"OPERATE_INFLOW_OTHER"`
	OperateInflowBalance      float64        `json:"OPERATE_INFLOW_BALANCE"`
	TotalOperateInflow        float64        `json:"TOTAL_OPERATE_INFLOW"`
	BuyServices               float64        `json:"BUY_SERVICES"`
	LoanAdvanceAdd            float64        `json:"LOAN_ADVANCE_ADD"`
	PbcInterbankAdd           float64        `json:"PBC_INTERBANK_ADD"`
	PayOrigicCompensate       float64        `json:"PAY_ORIGIC_COMPENSATE"`
	PayInterestCommission     float64        `json:"PAY_INTEREST_COMMISSION"`
	PayPolicyBonus            float64        `json:"PAY_POLICY_BONUS"`
	PayStaffCash              float64        `json:"PAY_STAFF_CASH"`
	PayAllTax                 float64        `json:"PAY_ALL_TAX"`
	PayOtherOperate           float64        `json:"PAY_OTHER_OPERATE"`
	OperateOutflowOther       float64        `json:"OPERATE_OUTFLOW_OTHER"`
	OperateOutflowBalance     float64        `json:"OPERATE_OUTFLOW_BALANCE"`
	TotalOperateOutflow       float64        `json:"TOTAL_OPERATE_OUTFLOW"`
	OperateNetcashOther       float64        `json:"OPERATE_NETCASH_OTHER"`
	OperateNetcashBalance     float64        `json:"OPERATE_NETCASH_BALANCE"`
	// 经营活动产生的现金流量净额
	NetcashOperate           float64 `json:"NETCASH_OPERATE"`
	WithdrawInvest           float64 `json:"WITHDRAW_INVEST"`
	ReceiveInvestIncome      float64 `json:"RECEIVE_INVEST_INCOME"`
	DisposalLongAsset        float64 `json:"DISPOSAL_LONG_ASSET"`
	DisposalSubsidiaryOther  float64 `json:"DISPOSAL_SUBSIDIARY_OTHER"`
	ReducePledgeTimedeposits float64 `json:"REDUCE_PLEDGE_TIMEDEPOSITS"`
	ReceiveOtherInvest       float64 `json:"RECEIVE_OTHER_INVEST"`
	InvestInflowOther        float64 `json:"INVEST_INFLOW_OTHER"`
	InvestInflowBalance      float64 `json:"INVEST_INFLOW_BALANCE"`
	TotalInvestInflow        float64 `json:"TOTAL_INVEST_INFLOW"`
	ConstructLongAsset       float64 `json:"CONSTRUCT_LONG_ASSET"`
	InvestPayCash            float64 `json:"INVEST_PAY_CASH"`
	PledgeLoanAdd            float64 `json:"PLEDGE_LOAN_ADD"`
	ObtainSubsidiaryOther    float64 `json:"OBTAIN_SUBSIDIARY_OTHER"`
	AddPledgeTimedeposits    float64 `json:"ADD_PLEDGE_TIMEDEPOSITS"`
	PayOtherInvest           float64 `json:"PAY_OTHER_INVEST"`
	InvestOutflowOther       float64 `json:"INVEST_OUTFLOW_OTHER"`
	InvestOutflowBalance     float64 `json:"INVEST_OUTFLOW_BALANCE"`
	TotalInvestOutflow       float64 `json:"TOTAL_INVEST_OUTFLOW"`
	InvestNetcashOther       float64 `json:"INVEST_NETCASH_OTHER"`
	InvestNetcashBalance     float64 `json:"INVEST_NETCASH_BALANCE"`
	// 投资活动产生的现金流量净额
	NetcashInvest          float64 `json:"NETCASH_INVEST"`
	AcceptInvestCash       float64 `json:"ACCEPT_INVEST_CASH"`
	SubsidiaryAcceptInvest float64 `json:"SUBSIDIARY_ACCEPT_INVEST"`
	ReceiveLoanCash        float64 `json:"RECEIVE_LOAN_CASH"`
	IssueBond              float64 `json:"ISSUE_BOND"`
	ReceiveOtherFinance    float64 `json:"RECEIVE_OTHER_FINANCE"`
	FinanceInflowOther     float64 `json:"FINANCE_INFLOW_OTHER"`
	FinanceInflowBalance   float64 `json:"FINANCE_INFLOW_BALANCE"`
	TotalFinanceInflow     float64 `json:"TOTAL_FINANCE_INFLOW"`
	PayDebtCash            float64 `json:"PAY_DEBT_CASH"`
	AssignDividendPorfit   float64 `json:"ASSIGN_DIVIDEND_PORFIT"`
	SubsidiaryPayDividend  float64 `json:"SUBSIDIARY_PAY_DIVIDEND"`
	BuySubsidiaryEquity    float64 `json:"BUY_SUBSIDIARY_EQUITY"`
	PayOtherFinance        float64 `json:"PAY_OTHER_FINANCE"`
	SubsidiaryReduceCash   float64 `json:"SUBSIDIARY_REDUCE_CASH"`
	FinanceOutflowOther    float64 `json:"FINANCE_OUTFLOW_OTHER"`
	FinanceOutflowBalance  float64 `json:"FINANCE_OUTFLOW_BALANCE"`
	TotalFinanceOutflow    float64 `json:"TOTAL_FINANCE_OUTFLOW"`
	FinanceNetcashOther    float64 `json:"FINANCE_NETCASH_OTHER"`
	FinanceNetcashBalance  float64 `json:"FINANCE_NETCASH_BALANCE"`
	// 筹资活动产生的现金流量净额
	NetcashFinance               float64 `json:"NETCASH_FINANCE"`
	RateChangeEffect             float64 `json:"RATE_CHANGE_EFFECT"`
	CceAddOther                  float64 `json:"CCE_ADD_OTHER"`
	CceAddBalance                float64 `json:"CCE_ADD_BALANCE"`
	CceAdd                       float64 `json:"CCE_ADD"`
	BeginCce                     float64 `json:"BEGIN_CCE"`
	EndCceOther                  float64 `json:"END_CCE_OTHER"`
	EndCceBalance                float64 `json:"END_CCE_BALANCE"`
	EndCce                       float64 `json:"END_CCE"`
	Netprofit                    float64 `json:"NETPROFIT"`
	AssetImpairment              float64 `json:"ASSET_IMPAIRMENT"`
	FaIrDepr                     float64 `json:"FA_IR_DEPR"`
	OilgasBiologyDepr            float64 `json:"OILGAS_BIOLOGY_DEPR"`
	IrDepr                       float64 `json:"IR_DEPR"`
	IaAmortize                   float64 `json:"IA_AMORTIZE"`
	LpeAmortize                  float64 `json:"LPE_AMORTIZE"`
	DeferIncomeAmortize          float64 `json:"DEFER_INCOME_AMORTIZE"`
	PrepaidExpenseReduce         float64 `json:"PREPAID_EXPENSE_REDUCE"`
	AccruedExpenseAdd            float64 `json:"ACCRUED_EXPENSE_ADD"`
	DisposalLongassetLoss        float64 `json:"DISPOSAL_LONGASSET_LOSS"`
	FaScrapLoss                  float64 `json:"FA_SCRAP_LOSS"`
	FairvalueChangeLoss          float64 `json:"FAIRVALUE_CHANGE_LOSS"`
	FinanceExpense               float64 `json:"FINANCE_EXPENSE"`
	InvestLoss                   float64 `json:"INVEST_LOSS"`
	DeferTax                     float64 `json:"DEFER_TAX"`
	DtAssetReduce                float64 `json:"DT_ASSET_REDUCE"`
	DtLiabAdd                    float64 `json:"DT_LIAB_ADD"`
	PredictLiabAdd               float64 `json:"PREDICT_LIAB_ADD"`
	InventoryReduce              float64 `json:"INVENTORY_REDUCE"`
	OperateReceReduce            float64 `json:"OPERATE_RECE_REDUCE"`
	OperatePayableAdd            float64 `json:"OPERATE_PAYABLE_ADD"`
	Other                        float64 `json:"OTHER"`
	OperateNetcashOthernote      float64 `json:"OPERATE_NETCASH_OTHERNOTE"`
	OperateNetcashBalancenote    float64 `json:"OPERATE_NETCASH_BALANCENOTE"`
	NetcashOperatenote           float64 `json:"NETCASH_OPERATENOTE"`
	DebtTransferCapital          float64 `json:"DEBT_TRANSFER_CAPITAL"`
	ConvertBond1Year             float64 `json:"CONVERT_BOND_1YEAR"`
	FinleaseObtainFa             float64 `json:"FINLEASE_OBTAIN_FA"`
	UninvolveInvestfinOther      float64 `json:"UNINVOLVE_INVESTFIN_OTHER"`
	EndCash                      float64 `json:"END_CASH"`
	BeginCash                    float64 `json:"BEGIN_CASH"`
	EndCashEquivalents           float64 `json:"END_CASH_EQUIVALENTS"`
	BeginCashEquivalents         float64 `json:"BEGIN_CASH_EQUIVALENTS"`
	CceAddOthernote              float64 `json:"CCE_ADD_OTHERNOTE"`
	CceAddBalancenote            float64 `json:"CCE_ADD_BALANCENOTE"`
	CceAddnote                   float64 `json:"CCE_ADDNOTE"`
	SalesServicesYoy             float64 `json:"SALES_SERVICES_YOY"`
	DepositInterbankAddYoy       float64 `json:"DEPOSIT_INTERBANK_ADD_YOY"`
	LoanPbcAddYoy                float64 `json:"LOAN_PBC_ADD_YOY"`
	OfiBfAddYoy                  float64 `json:"OFI_BF_ADD_YOY"`
	ReceiveOrigicPremiumYoy      float64 `json:"RECEIVE_ORIGIC_PREMIUM_YOY"`
	ReceiveReinsureNetYoy        float64 `json:"RECEIVE_REINSURE_NET_YOY"`
	InsuredInvestAddYoy          float64 `json:"INSURED_INVEST_ADD_YOY"`
	DisposalTfaAddYoy            float64 `json:"DISPOSAL_TFA_ADD_YOY"`
	ReceiveInterestCommissionYoy float64 `json:"RECEIVE_INTEREST_COMMISSION_YOY"`
	BorrowFundAddYoy             float64 `json:"BORROW_FUND_ADD_YOY"`
	LoanAdvanceReduceYoy         float64 `json:"LOAN_ADVANCE_REDUCE_YOY"`
	RepoBusinessAddYoy           float64 `json:"REPO_BUSINESS_ADD_YOY"`
	ReceiveTaxRefundYoy          float64 `json:"RECEIVE_TAX_REFUND_YOY"`
	ReceiveOtherOperateYoy       float64 `json:"RECEIVE_OTHER_OPERATE_YOY"`
	OperateInflowOtherYoy        float64 `json:"OPERATE_INFLOW_OTHER_YOY"`
	OperateInflowBalanceYoy      float64 `json:"OPERATE_INFLOW_BALANCE_YOY"`
	TotalOperateInflowYoy        float64 `json:"TOTAL_OPERATE_INFLOW_YOY"`
	BuyServicesYoy               float64 `json:"BUY_SERVICES_YOY"`
	LoanAdvanceAddYoy            float64 `json:"LOAN_ADVANCE_ADD_YOY"`
	PbcInterbankAddYoy           float64 `json:"PBC_INTERBANK_ADD_YOY"`
	PayOrigicCompensateYoy       float64 `json:"PAY_ORIGIC_COMPENSATE_YOY"`
	PayInterestCommissionYoy     float64 `json:"PAY_INTEREST_COMMISSION_YOY"`
	PayPolicyBonusYoy            float64 `json:"PAY_POLICY_BONUS_YOY"`
	PayStaffCashYoy              float64 `json:"PAY_STAFF_CASH_YOY"`
	PayAllTaxYoy                 float64 `json:"PAY_ALL_TAX_YOY"`
	PayOtherOperateYoy           float64 `json:"PAY_OTHER_OPERATE_YOY"`
	OperateOutflowOtherYoy       float64 `json:"OPERATE_OUTFLOW_OTHER_YOY"`
	OperateOutflowBalanceYoy     float64 `json:"OPERATE_OUTFLOW_BALANCE_YOY"`
	TotalOperateOutflowYoy       float64 `json:"TOTAL_OPERATE_OUTFLOW_YOY"`
	OperateNetcashOtherYoy       float64 `json:"OPERATE_NETCASH_OTHER_YOY"`
	OperateNetcashBalanceYoy     float64 `json:"OPERATE_NETCASH_BALANCE_YOY"`
	NetcashOperateYoy            float64 `json:"NETCASH_OPERATE_YOY"`
	WithdrawInvestYoy            float64 `json:"WITHDRAW_INVEST_YOY"`
	ReceiveInvestIncomeYoy       float64 `json:"RECEIVE_INVEST_INCOME_YOY"`
	DisposalLongAssetYoy         float64 `json:"DISPOSAL_LONG_ASSET_YOY"`
	DisposalSubsidiaryOtherYoy   float64 `json:"DISPOSAL_SUBSIDIARY_OTHER_YOY"`
	ReducePledgeTimedepositsYoy  float64 `json:"REDUCE_PLEDGE_TIMEDEPOSITS_YOY"`
	ReceiveOtherInvestYoy        float64 `json:"RECEIVE_OTHER_INVEST_YOY"`
	InvestInflowOtherYoy         float64 `json:"INVEST_INFLOW_OTHER_YOY"`
	InvestInflowBalanceYoy       float64 `json:"INVEST_INFLOW_BALANCE_YOY"`
	TotalInvestInflowYoy         float64 `json:"TOTAL_INVEST_INFLOW_YOY"`
	ConstructLongAssetYoy        float64 `json:"CONSTRUCT_LONG_ASSET_YOY"`
	InvestPayCashYoy             float64 `json:"INVEST_PAY_CASH_YOY"`
	PledgeLoanAddYoy             float64 `json:"PLEDGE_LOAN_ADD_YOY"`
	ObtainSubsidiaryOtherYoy     float64 `json:"OBTAIN_SUBSIDIARY_OTHER_YOY"`
	AddPledgeTimedepositsYoy     float64 `json:"ADD_PLEDGE_TIMEDEPOSITS_YOY"`
	PayOtherInvestYoy            float64 `json:"PAY_OTHER_INVEST_YOY"`
	InvestOutflowOtherYoy        float64 `json:"INVEST_OUTFLOW_OTHER_YOY"`
	InvestOutflowBalanceYoy      float64 `json:"INVEST_OUTFLOW_BALANCE_YOY"`
	TotalInvestOutflowYoy        float64 `json:"TOTAL_INVEST_OUTFLOW_YOY"`
	InvestNetcashOtherYoy        float64 `json:"INVEST_NETCASH_OTHER_YOY"`
	InvestNetcashBalanceYoy      float64 `json:"INVEST_NETCASH_BALANCE_YOY"`
	NetcashInvestYoy             float64 `json:"NETCASH_INVEST_YOY"`
	AcceptInvestCashYoy          float64 `json:"ACCEPT_INVEST_CASH_YOY"`
	SubsidiaryAcceptInvestYoy    float64 `json:"SUBSIDIARY_ACCEPT_INVEST_YOY"`
	ReceiveLoanCashYoy           float64 `json:"RECEIVE_LOAN_CASH_YOY"`
	IssueBondYoy                 float64 `json:"ISSUE_BOND_YOY"`
	ReceiveOtherFinanceYoy       float64 `json:"RECEIVE_OTHER_FINANCE_YOY"`
	FinanceInflowOtherYoy        float64 `json:"FINANCE_INFLOW_OTHER_YOY"`
	FinanceInflowBalanceYoy      float64 `json:"FINANCE_INFLOW_BALANCE_YOY"`
	TotalFinanceInflowYoy        float64 `json:"TOTAL_FINANCE_INFLOW_YOY"`
	PayDebtCashYoy               float64 `json:"PAY_DEBT_CASH_YOY"`
	AssignDividendPorfitYoy      float64 `json:"ASSIGN_DIVIDEND_PORFIT_YOY"`
	SubsidiaryPayDividendYoy     float64 `json:"SUBSIDIARY_PAY_DIVIDEND_YOY"`
	BuySubsidiaryEquityYoy       float64 `json:"BUY_SUBSIDIARY_EQUITY_YOY"`
	PayOtherFinanceYoy           float64 `json:"PAY_OTHER_FINANCE_YOY"`
	SubsidiaryReduceCashYoy      float64 `json:"SUBSIDIARY_REDUCE_CASH_YOY"`
	FinanceOutflowOtherYoy       float64 `json:"FINANCE_OUTFLOW_OTHER_YOY"`
	FinanceOutflowBalanceYoy     float64 `json:"FINANCE_OUTFLOW_BALANCE_YOY"`
	TotalFinanceOutflowYoy       float64 `json:"TOTAL_FINANCE_OUTFLOW_YOY"`
	FinanceNetcashOtherYoy       float64 `json:"FINANCE_NETCASH_OTHER_YOY"`
	FinanceNetcashBalanceYoy     float64 `json:"FINANCE_NETCASH_BALANCE_YOY"`
	NetcashFinanceYoy            float64 `json:"NETCASH_FINANCE_YOY"`
	RateChangeEffectYoy          float64 `json:"RATE_CHANGE_EFFECT_YOY"`
	CceAddOtherYoy               float64 `json:"CCE_ADD_OTHER_YOY"`
	CceAddBalanceYoy             float64 `json:"CCE_ADD_BALANCE_YOY"`
	CceAddYoy                    float64 `json:"CCE_ADD_YOY"`
	BeginCceYoy                  float64 `json:"BEGIN_CCE_YOY"`
	EndCceOtherYoy               float64 `json:"END_CCE_OTHER_YOY"`
	EndCceBalanceYoy             float64 `json:"END_CCE_BALANCE_YOY"`
	EndCceYoy                    float64 `json:"END_CCE_YOY"`
	NetprofitYoy                 float64 `json:"NETPROFIT_YOY"`
	AssetImpairmentYoy           float64 `json:"ASSET_IMPAIRMENT_YOY"`
	FaIrDeprYoy                  float64 `json:"FA_IR_DEPR_YOY"`
	OilgasBiologyDeprYoy         float64 `json:"OILGAS_BIOLOGY_DEPR_YOY"`
	IrDeprYoy                    float64 `json:"IR_DEPR_YOY"`
	IaAmortizeYoy                float64 `json:"IA_AMORTIZE_YOY"`
	LpeAmortizeYoy               float64 `json:"LPE_AMORTIZE_YOY"`
	DeferIncomeAmortizeYoy       float64 `json:"DEFER_INCOME_AMORTIZE_YOY"`
	PrepaidExpenseReduceYoy      float64 `json:"PREPAID_EXPENSE_REDUCE_YOY"`
	AccruedExpenseAddYoy         float64 `json:"ACCRUED_EXPENSE_ADD_YOY"`
	DisposalLongassetLossYoy     float64 `json:"DISPOSAL_LONGASSET_LOSS_YOY"`
	FaScrapLossYoy               float64 `json:"FA_SCRAP_LOSS_YOY"`
	FairvalueChangeLossYoy       float64 `json:"FAIRVALUE_CHANGE_LOSS_YOY"`
	FinanceExpenseYoy            float64 `json:"FINANCE_EXPENSE_YOY"`
	InvestLossYoy                float64 `json:"INVEST_LOSS_YOY"`
	DeferTaxYoy                  float64 `json:"DEFER_TAX_YOY"`
	DtAssetReduceYoy             float64 `json:"DT_ASSET_REDUCE_YOY"`
	DtLiabAddYoy                 float64 `json:"DT_LIAB_ADD_YOY"`
	PredictLiabAddYoy            float64 `json:"PREDICT_LIAB_ADD_YOY"`
	InventoryReduceYoy           float64 `json:"INVENTORY_REDUCE_YOY"`
	OperateReceReduceYoy         float64 `json:"OPERATE_RECE_REDUCE_YOY"`
	OperatePayableAddYoy         float64 `json:"OPERATE_PAYABLE_ADD_YOY"`
	OtherYoy                     float64 `json:"OTHER_YOY"`
	OperateNetcashOthernoteYoy   float64 `json:"OPERATE_NETCASH_OTHERNOTE_YOY"`
	OperateNetcashBalancenoteYoy float64 `json:"OPERATE_NETCASH_BALANCENOTE_YOY"`
	NetcashOperatenoteYoy        float64 `json:"NETCASH_OPERATENOTE_YOY"`
	DebtTransferCapitalYoy       float64 `json:"DEBT_TRANSFER_CAPITAL_YOY"`
	ConvertBond1YearYoy          float64 `json:"CONVERT_BOND_1YEAR_YOY"`
	FinleaseObtainFaYoy          float64 `json:"FINLEASE_OBTAIN_FA_YOY"`
	UninvolveInvestfinOtherYoy   float64 `json:"UNINVOLVE_INVESTFIN_OTHER_YOY"`
	EndCashYoy                   float64 `json:"END_CASH_YOY"`
	BeginCashYoy                 float64 `json:"BEGIN_CASH_YOY"`
	EndCashEquivalentsYoy        float64 `json:"END_CASH_EQUIVALENTS_YOY"`
	BeginCashEquivalentsYoy      float64 `json:"BEGIN_CASH_EQUIVALENTS_YOY"`
	CceAddOthernoteYoy           float64 `json:"CCE_ADD_OTHERNOTE_YOY"`
	CceAddBalancenoteYoy         float64 `json:"CCE_ADD_BALANCENOTE_YOY"`
	CceAddnoteYoy                float64 `json:"CCE_ADDNOTE_YOY"`
	OpinionType                  string  `json:"OPINION_TYPE"`
	OsopinionType                string  `json:"OSOPINION_TYPE"`
	MinorityInterest             float64 `json:"MINORITY_INTEREST"`
	MinorityInterestYoy          float64 `json:"MINORITY_INTEREST_YOY"`
}

// CashflowDataList cashflow 列表
type CashflowDataList []CashflowData

// RespFinaCashflowData 现金流量接口返回数据
type RespFinaCashflowData struct {
	Version string `json:"version"`
	Result  struct {
		Pages int              `json:"pages"`
		Data  CashflowDataList `json:"data"`
		Count int              `json:"count"`
	} `json:"result"`
	Success bool   `json:"success"`
	Message string `json:"message"`
	Code    int    `json:"code"`
}

// QueryFinaCashflowData 获取财务分析现金流量表数据，最新数据在最前面
func (e EastMoney) QueryFinaCashflowData(ctx context.Context, secuCode string) (CashflowDataList, error) {
	apiurl := "https://datacenter.eastmoney.com/securities/api/data/get"
	params := map[string]string{
		"source": "HSF10",
		"client": "APP",
		"type":   "RPT_F10_FINANCE_GCASHFLOW",
		"sty":    "APP_F10_GCASHFLOW",
		"filter": fmt.Sprintf(`(SECUCODE="%s")`, strings.ToUpper(secuCode)),
		"ps":     "10",
		"sr":     "-1",
		"st":     "REPORT_DATE",
	}
	logging.Debug(ctx, "EastMoney QueryFinaCashflowData "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	resp := RespFinaCashflowData{}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, nil, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFinaCashflowData "+apiurl+" end",
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
