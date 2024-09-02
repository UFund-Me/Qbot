// Package models
// 全局变量

package models

import (
	"encoding/json"
	"io/ioutil"
	"time"

	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/logging"
)

var (
	// StockIndustryList 东方财富股票行业列表
	StockIndustryList []string
	// FundTypeList 基金类型列表
	FundTypeList []string
	// Fund4433TypeList 4433基金类型列表
	Fund4433TypeList []string
	// FundAllList 全量基金列表
	FundAllList FundList
	// Fund4433List 满足4433法则的基金列表
	Fund4433List FundList
	// FundManagers 基金经理列表
	FundManagers eastmoney.FundManagerInfoList
	// SyncFundTime 基金数据同步时间
	SyncFundTime = time.Now()
	// RawFundAllListFilename api返回的原始结果
	RawFundAllListFilename = "./eastmoney_funds_list.json"
	// FundAllListFilename 基金列表数据文件
	FundAllListFilename = "./fund_all_list.json"
	// Fund4433ListFilename 4433基金列表数据文件
	Fund4433ListFilename = "./fund_4433_list.json"
	// IndustryListFilename 行业列表数据文件
	IndustryListFilename = "./industry_list.json"
	// FundTypeListFilename 基金类型数据文件
	FundTypeListFilename = "./fund_type_list.json"
	// FundManagersFilename 基金经理数据文件
	FundManagersFilename = "./fund_managers.json"
	// AAACompanyBondSyl AAA公司债当期收益率
	AAACompanyBondSyl = -1.0 // datacenter.ChinaBond.QueryAAACompanyBondSyl(context.Background())
)

// InitGlobalVars 初始化全局变量
func InitGlobalVars() {
	if err := InitIndustryList(); err != nil {
		logging.Error(nil, "init models global vars error:"+err.Error())
	}
	if err := InitFundAllList(); err != nil {
		logging.Error(nil, "init models global vars error:"+err.Error())
	}
	if err := InitFund4433List(); err != nil {
		logging.Error(nil, "init models global vars error:"+err.Error())
	}
	if err := InitFundTypeList(); err != nil {
		logging.Error(nil, "init models global vars error:"+err.Error())
	}
	if err := InitFundManagers(); err != nil {
		logging.Error(nil, "init models global vars error:"+err.Error())
	}
	// 更新同步时间
	SyncFundTime = time.Now()
}

// InitIndustryList 初始化行业列表
func InitIndustryList() error {
	indlist, err := ioutil.ReadFile(IndustryListFilename)
	if err != nil {
		return err
	}
	return json.Unmarshal(indlist, &StockIndustryList)
}

// InitFundAllList 从json文件加载基金列表
func InitFundAllList() error {
	fundlist, err := ioutil.ReadFile(FundAllListFilename)
	if err != nil {
		return err
	}
	return json.Unmarshal(fundlist, &FundAllList)
}

// InitFund4433List 从json文件加载基金列表
func InitFund4433List() error {
	fundlist, err := ioutil.ReadFile(Fund4433ListFilename)
	if err != nil {
		return err
	}
	if err := json.Unmarshal(fundlist, &Fund4433List); err != nil {
		return err
	}
	Fund4433List.Sort(FundSortTypeWeek)
	Fund4433TypeList = Fund4433List.Types()
	return nil
}

// InitFundTypeList 从json文件加载基金类型
func InitFundTypeList() error {
	types, err := ioutil.ReadFile(FundTypeListFilename)
	if err != nil {
		return err
	}
	return json.Unmarshal(types, &FundTypeList)
}

// InitFundManagers 初始化基金经理列表
func InitFundManagers() error {
	m, err := ioutil.ReadFile(FundManagersFilename)
	if err != nil {
		return err
	}
	return json.Unmarshal(m, &FundManagers)
}
