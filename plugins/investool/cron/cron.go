// Package cron 定时任务
package cron

import (
	"time"

	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/logging"
	"github.com/go-co-op/gocron"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/spf13/viper"
)

var (
	promSyncLabels = []string{
		"jobname",
	}
	promSyncError = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Namespace: "cron",
			Name:      "sync_error",
			Help:      "cron sync job error",
		}, promSyncLabels,
	)
)

// RunCronJobs 启动定时任务
func RunCronJobs(async bool) {
	timezone, err := time.LoadLocation("Asia/Shanghai")
	if err != nil {
		logging.Errorf(nil, "RunCronJobs time LoadLocation error:%v, using Local timezone as default", err.Error())
		timezone, _ = time.LoadLocation("Local")
	}
	logging.Debugf(nil, "cron timezone:%v", timezone)
	sched := gocron.NewScheduler(timezone)

	// 同步基金净值列表和4433列表
	// sched.Cron(viper.GetString("app.cronexp.sync_fund")).Do(SyncFund)
	// 同步东方财富行业列表
	// sched.Cron(viper.GetString("app.cronexp.sync_industry_list")).Do(SyncIndustryList)
	// 同步基金经理列表
	// sched.Cron(viper.GetString("app.cronexp.sync_fund_managers")).Do(SyncFundManagers)

	// ----------------------
	// 以上的定时任务注释掉不再执行是因为部署的机器内存不够，执行时会oom
	// 改为定时读取本地的JSON数据更新到全局变量，json数据由外部同步到机器上
	sched.Cron(viper.GetString("app.cronexp.sync_global_vars")).Do(models.InitGlobalVars)

	if async {
		sched.StartAsync()
	} else {
		sched.StartBlocking()
	}
}
