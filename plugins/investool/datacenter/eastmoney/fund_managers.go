// 天天基金获取基金经理列表(web接口)
// https://fund.eastmoney.com/manager/jjjl_all_penavgrowth_desc.html

package eastmoney

import (
	"context"
	"fmt"
	"math"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/corpix/uarand"
	"go.uber.org/zap"
)

// FundManagerInfo 基金经理信息
type FundManagerInfo struct {
	// ID
	ID string `json:"id"`
	// 姓名
	Name string `json:"name"`
	// 基金公司id
	FundCompanyID string `json:"fund_company_id"`
	// 基金公司名称
	FundCompanyName string `json:"fund_company_name"`
	// 现任基金代码列表
	FundCodes []string `json:"fund_codes"`
	// 现任基金名称列表
	FundNames []string `json:"fund_names"`
	// 累计从业年限
	WorkingYears float64 `json:"working_years"`
	// 现任基金最佳回报（%）
	CurrentBestReturn float64 `json:"current_best_return"`
	// 现任最佳基金代码(PRECODE)
	CurrentBestFundCode string `json:"current_best_fund_code"`
	// 现任最佳基金名称(PRENAME)
	CurrentBestFundName string `json:"current_best_fund_name"`
	// 现任基金资产总规模（亿元）
	CurrentFundScale float64 `json:"current_fund_scale"`
	// 任职期间最佳基金回报（%）
	WorkingBestReturn float64 `json:"working_best_return"`
	// 年化回报（%）
	Yieldse float64 `json:"yieldse"`
	// 擅长领域
	CurrentBestFundType string `json:"current_best_fund_type"`
	// 业绩评分
	Score float64 `json:"score"`
	// 个人简介 + 投资方法 + 投资理念
	Resume string `json:"resume"`
	// 获奖数
	AwardNum int `json:"award_num"`
}

// FundManagerInfoList 基金经理列表
type FundManagerInfoList []*FundManagerInfo

// ParamFundManagerFilter 基金列表过滤参数
type ParamFundManagerFilter struct {
	// 指定名字搜索
	Name string
	// 最低从业年限
	MinWorkingYears int `json:"min_working_years"`
	// 最低年化回报（%）
	MinYieldse float64 `json:"min_yieldse"`
	// 最大现任基金数量
	MaxCurrentFundCount int `json:"max_current_fund_count"`
	// 最小管理规模（亿）
	MinScale float64 `json:"min_scale"`
	// 擅长基金分类
	FundType string `json:"fund_type"`
}

// Filter 按条件过滤列表
func (f FundManagerInfoList) Filter(ctx context.Context, p ParamFundManagerFilter) FundManagerInfoList {
	result := FundManagerInfoList{}
	for _, i := range f {
		if p.Name != "" && p.Name != i.Name {
			continue
		}
		if p.FundType != "" && p.FundType != i.CurrentBestFundType {
			continue
		}
		if i.WorkingYears < float64(p.MinWorkingYears) {
			continue
		}
		if i.Yieldse < p.MinYieldse {
			continue
		}
		if len(i.FundCodes) > p.MaxCurrentFundCount {
			continue
		}
		if i.CurrentFundScale < p.MinScale {
			continue
		}
		result = append(result, i)
	}
	return result
}

// SortByFundCount 列表按 管理基金数 排序
func (f FundManagerInfoList) SortByFundCount() {
	sort.Slice(f, func(i, j int) bool {
		return len(f[i].FundCodes) > len(f[j].FundCodes)
	})
}

// SortByAwardNum 列表按 获奖数 排序
func (f FundManagerInfoList) SortByAwardNum() {
	sort.Slice(f, func(i, j int) bool {
		return f[i].AwardNum > f[j].AwardNum
	})
}

// SortByScore 列表按 业绩评分 排序
func (f FundManagerInfoList) SortByScore() {
	sort.Slice(f, func(i, j int) bool {
		return f[i].Score > f[j].Score
	})
}

// SortByScale 列表按 基金规模 排序
func (f FundManagerInfoList) SortByScale() {
	sort.Slice(f, func(i, j int) bool {
		return f[i].CurrentFundScale > f[j].CurrentFundScale
	})
}

// SortByCurrentBestReturn 列表按 现任基金最佳回报 排序
func (f FundManagerInfoList) SortByCurrentBestReturn() {
	sort.Slice(f, func(i, j int) bool {
		return f[i].CurrentBestReturn > f[j].CurrentBestReturn
	})
}

// SortByWorkingBestReturn 列表按 任职基金最佳回报 排序
func (f FundManagerInfoList) SortByWorkingBestReturn() {
	sort.Slice(f, func(i, j int) bool {
		return f[i].WorkingBestReturn > f[j].WorkingBestReturn
	})
}

// SortByYieldse 列表按 年化回报 排序
func (f FundManagerInfoList) SortByYieldse() {
	sort.Slice(f, func(i, j int) bool {
		return f[i].Yieldse > f[j].Yieldse
	})
}

// FundMangers 查询基金经理列表（web接口）
// ft（基金类型） all:全部 gp:股票型 hh:混合型 zq:债券型 sy:收益型
// sc（排序字段）abbname:经理名 jjgspy:基金公司 totaldays:从业时间 netnav:基金规模 penavgrowth:现任基金最佳回报
// st（排序类型）asc desc
func (e EastMoney) FundMangers(ctx context.Context, ft, sc, st string) (FundManagerInfoList, error) {
	beginTime := time.Now()
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	result := []*FundManagerInfo{}
	index := 1
	for {
		apiurl := fmt.Sprintf(
			"http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=%s&pn=20&pi=%d&sc=%s&st=%s",
			ft,
			index,
			sc,
			st,
		)
		logging.Debug(ctx, "EastMoney FundMangers "+apiurl+" begin", zap.Int("index", index))
		beginTime := time.Now()
		resp, err := goutils.HTTPGETRaw(ctx, e.HTTPClient, apiurl, header)
		strresp := string(resp)
		latency := time.Now().Sub(beginTime).Milliseconds()
		logging.Debug(ctx, "EastMoney FundMangers "+apiurl+" end",
			zap.Int64("latency(ms)", latency),
			zap.Int("index", index),
		)
		if err != nil {
			return nil, err
		}
		reg, err := regexp.Compile(`\[(".+?")\]`)
		if err != nil {
			logging.Error(ctx, "regexp error:"+err.Error())
			return nil, err
		}
		matched := reg.FindAllStringSubmatch(strresp, -1)
		if len(matched) == 0 {
			break
		}

		var mwg sync.WaitGroup
		var mlock sync.Mutex
		// 每页20只基金，并发内存不够可以先考虑每页获取少一点看看效果
		field, _ := regexp.Compile(`"(.*?)"`)
		for _, m := range matched {
			mwg.Add(1)
			go func(m1 string) {
				// "30057445","张少华","80000200","中银证券","009640,009641,010892,010893,501095","中银证券优选行业龙头混合A,中银证券优选行业龙头混合C,中银证券精选行业股票A,中银证券精选行业股票C,中银证券科创3年封闭混合","3993","26.52%","009640","中银证券优选行业龙头混合A","28.43亿元","82.97%"
				defer mwg.Done()

				fields := field.FindAllStringSubmatch(m1, -1)
				if len(fields) != 12 {
					logging.Warnf(ctx, "invalid fields len:%v %v", len(fields), m1)
					return
				}
				totaldays := 0
				if fields[6][1] != "" && fields[6][1] != "--" {
					totaldays, err = strconv.Atoi(fields[6][1])
					if err != nil {
						logging.Warnf(ctx, "parse totaldays:%v to int error:%v", fields[6], err)
					}
				}
				bestReturn := 0.0
				if fields[7][1] != "" && fields[7][1] != "--" {
					bestReturnNum := strings.TrimSuffix(fields[7][1], "%")
					bestReturn, err = strconv.ParseFloat(bestReturnNum, 64)
					if err != nil {
						logging.Warnf(ctx, "parse bestReturn:%v to float64 error:%v", bestReturnNum, err)
					}
				}
				scale := 0.0
				if fields[10][1] != "" && fields[10][1] != "--" {
					scaleNum := strings.TrimSuffix(fields[10][1], "亿元")
					scale, err = strconv.ParseFloat(scaleNum, 64)
					if err != nil {
						logging.Warnf(ctx, "parse scale:%v to float64 error:%v", scaleNum, err)
					}
				}
				wbestReturn := 0.0
				if fields[11][1] != "" && fields[11][1] != "--" {
					wbestReturnNum := strings.TrimSuffix(fields[11][1], "%")
					wbestReturn, err = strconv.ParseFloat(wbestReturnNum, 64)
					if err != nil {
						logging.Warnf(ctx, "parse bestReturn:%v to float64 error:%v", wbestReturnNum, err)
					}
				}
				currentBestFundCode := fields[8][1]
				currentBestFundName := fields[9][1]
				currentBestFundType := ""
				yieldse := 0.0
				score := 0.0
				awardNum := 0
				resume := ""

				info, err := e.QueryFundMsnMangerInfo(ctx, fields[0][1])
				if err != nil {
					logging.Error(ctx, "QueryFundMsnMangerInfo err:"+err.Error())
				} else {
					resume = strings.TrimSpace(fmt.Sprintf("%s\n投资方法:%s\n投资理念:%s", info.Datas.Resume, info.Datas.Investmentmethod, info.Datas.Investmentidear))
					currentBestFundType = MftypeDesc[info.Datas.Mftype]

					if info.Datas.Yieldse != "" && info.Datas.Yieldse != "--" {
						yieldse, err = strconv.ParseFloat(info.Datas.Yieldse, 64)
						if err != nil {
							logging.Warnf(ctx, "parse yieldse:%v to float64 error:%v", info.Datas.Yieldse, err)
						}
					}
					// msn info里面的代表基金可能会不一样，以msn里面的为准
					if info.Datas.Precode != "" && info.Datas.Precode != "--" {
						currentBestFundCode = info.Datas.Precode
						currentBestFundName = info.Datas.Prename
					}
					if info.Datas.Mgold != "" && info.Datas.Mgold != "--" {
						score, err = strconv.ParseFloat(info.Datas.Mgold, 64)
						if err != nil {
							logging.Error(ctx, "parse Mgold to score error:"+err.Error())
						}
					}
					if info.Datas.Awardnum != "" && info.Datas.Awardnum != "--" {
						awardNum, err = strconv.Atoi(info.Datas.Awardnum)
						if err != nil {
							logging.Error(ctx, "parse Awardnum error:"+err.Error())
						}
					}
				}
				mlock.Lock()
				result = append(result, &FundManagerInfo{
					ID:                  fields[0][1],
					Name:                fields[1][1],
					FundCompanyID:       fields[2][1],
					FundCompanyName:     fields[3][1],
					FundCodes:           strings.Split(fields[4][1], ","),
					FundNames:           strings.Split(fields[5][1], ","),
					WorkingYears:        math.Round(float64(totaldays) / 365.0),
					CurrentBestReturn:   bestReturn,
					CurrentBestFundCode: currentBestFundCode,
					CurrentBestFundName: currentBestFundName,
					CurrentFundScale:    scale,
					WorkingBestReturn:   wbestReturn,
					Yieldse:             yieldse,
					CurrentBestFundType: currentBestFundType,
					Score:               score,
					Resume:              resume,
					AwardNum:            awardNum,
				})
				mlock.Unlock()
			}(m[1])
		}
		mwg.Wait()
		// 等20个goroutine全部完了再开始新的，不然内存可能不够
		index++
	}
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney FundMangers end",
		zap.Int64("latency(ms)", latency),
		zap.Int("resultCount", len(result)),
	)
	return result, nil
}
