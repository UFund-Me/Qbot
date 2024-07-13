// Package cron 定时任务
package cron

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/investool/core"
	"github.com/axiaoxin-com/investool/datacenter"
	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/logging"
)

// SyncFund 同步基金数据
func SyncFund() {
	if !goutils.IsTradingDay() {
		return
	}
	ctx := context.Background()
	logging.Info(ctx, "SyncFund request start...")

	// 获取全量列表
	efundlist, err := datacenter.EastMoney.QueryAllFundList(ctx, eastmoney.FundTypeALL)
	if err != nil {
		logging.Error(ctx, "SyncFund QueryAllFundList error:"+err.Error())
		promSyncError.WithLabelValues("SyncFund").Inc()
		return
	}

	fundCodes := []string{}
	for _, efund := range efundlist {
		fundCodes = append(fundCodes, efund.Fcode)
	}
	s := core.NewSearcher(ctx)
	data, err := s.SearchFunds(ctx, fundCodes)
	fundlist := models.FundList{}
	typeMap := map[string]struct{}{}
	for _, fund := range data {
		fundlist = append(fundlist, fund)
		typeMap[fund.Type] = struct{}{}
	}

	// 更新 services 变量
	models.FundAllList = fundlist
	fundtypes := []string{}
	for k := range typeMap {
		fundtypes = append(fundtypes, k)
	}
	models.FundTypeList = fundtypes

	// 更新同步时间
	models.SyncFundTime = time.Now()

	// 更新4433列表
	Update4433()

	// 更新文件
	b, err := json.Marshal(efundlist)
	if err != nil {
		logging.Errorf(ctx, "SyncFund json marshal efundlist error:%v", err)
		promSyncError.WithLabelValues("SyncFund").Inc()
	} else if err := ioutil.WriteFile(models.RawFundAllListFilename, b, 0666); err != nil {
		logging.Errorf(ctx, "SyncFund WriteFile efundlist error:%v", err)
		promSyncError.WithLabelValues("SyncFund").Inc()
	}
	b, err = json.Marshal(fundlist)
	if err != nil {
		logging.Errorf(ctx, "SyncFund json marshal fundlist error:%v", err)
		promSyncError.WithLabelValues("SyncFund").Inc()
	} else if err := ioutil.WriteFile(models.FundAllListFilename, b, 0666); err != nil {
		logging.Errorf(ctx, "SyncFund WriteFile fundlist error:%v", err)
		promSyncError.WithLabelValues("SyncFund").Inc()
	}
	b, err = json.Marshal(models.FundTypeList)
	if err != nil {
		logging.Errorf(ctx, "SyncFund json marshal fundtypelist error:%v", err)
		promSyncError.WithLabelValues("SyncFund").Inc()
	} else if err := ioutil.WriteFile(models.FundTypeListFilename, b, 0666); err != nil {
		logging.Errorf(ctx, "SyncFund WriteFile fundtypelist error:%v", err)
		promSyncError.WithLabelValues("SyncFund").Inc()
	}
}

// Update4433 更新4433检测结果
func Update4433() {
	ctx := context.Background()
	fundlist := models.FundList{}
	for _, fund := range models.FundAllList {
		if fund.Is4433(ctx) {
			fundlist = append(fundlist, fund)
		}
	}
	// 更新 models 变量
	fundlist.Sort(models.FundSortTypeWeek)
	models.Fund4433List = fundlist

	// 更新文件
	b, err := json.Marshal(fundlist)
	if err != nil {
		logging.Errorf(ctx, "Update4433 json marshal error:", err)
		promSyncError.WithLabelValues("Update4433").Inc()
		return
	} else if err := ioutil.WriteFile(models.Fund4433ListFilename, b, 0666); err != nil {
		logging.Errorf(ctx, "Update4433 WriteFile error:", err)
		promSyncError.WithLabelValues("Update4433").Inc()
		return
	}
}
