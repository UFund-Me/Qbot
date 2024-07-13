// 天天基金获取基金详情

package eastmoney

import (
	"context"
	"fmt"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/corpix/uarand"
	"go.uber.org/zap"
)

// JJXQ 基金详情
type JJXQ struct {
	Datas struct {
		// 基金代码
		Fcode string `json:"FCODE"`
		// 基金名称
		Shortname string `json:"SHORTNAME"`
		// 基金类型中文描述
		Ftype string `json:"FTYPE"`
		// 成立时间
		Estabdate string `json:"ESTABDATE"`
		// 业绩比较基准
		Bench string `json:"BENCH"`
		// 资产规模（元）
		Endnav string `json:"ENDNAV"`
		// 规模截止日期
		Fegmrq string `json:"FEGMRQ"`
		// 基金评级
		RlevelSz string `json:"RLEVEL_SZ"`
		// 日涨幅 (%)
		Rzdf string `json:"RZDF"`
		// 单位净值
		Dwjz string `json:"DWJZ"`
		// 累计净值
		Ljjz string `json:"LJJZ"`
		// 当日确认份额时间点
		Currentdaymark string `json:"CURRENTDAYMARK"`
		// 购买起点（元）
		Minsg string `json:"MINSG"`
		// 首次购买（元）
		Minsbrg string `json:"MINSBRG"`
		// 追加购买（元）
		Minsbsg string `json:"MINSBSG"`
		// 定投起点（元）
		Mindt string `json:"MINDT"`
		// 单日累计购买上限（元）
		Maxsg string `json:"MAXSG"`
		// 申购状态
		Sgzt string `json:"SGZT"`
		// 卖出状态
		Shzt string `json:"SHZT"`
		// 定投状态 1:可定投
		Dtzt string `json:"DTZT"`
		// 原始购买费率
		Sourcerate string `json:"SOURCERATE"`
		// 实际购买费率
		Rate string `json:"RATE"`
		// 风险等级：4=中高风险 5=高风险
		Risklevel string `json:"RISKLEVEL"`
		// 跟踪标的代码
		Indexcode string `json:"INDEXCODE"`
		// 跟踪标的名称
		Indexname string `json:"INDEXNAME"`
		// 近1年波动率
		Stddev1 string `json:"STDDEV1"`
		// 近2年波动率
		Stddev2 string `json:"STDDEV2"`
		// 近3年波动率
		Stddev3 string `json:"STDDEV3"`
		// 近1年夏普比率
		Sharp1 string `json:"SHARP1"`
		// 近2年夏普比率
		Sharp2 string `json:"SHARP2"`
		// 近3年夏普比率
		Sharp3 string `json:"SHARP3"`
		// 近1年最大回撤
		Maxretra1 string `json:"MAXRETRA1"`
		// 买入确认日
		Ssbcfday string `json:"SSBCFDAY"`
	} `json:"Datas"`
}

// JDZF 阶段涨幅
type JDZF struct {
	Datas []struct {
		// Z:近1周 Y:近1月 3Y:近3月 6Y:近6月
		// 1N:近1年 2N:近2年 3N:近3年 5N:近五年
		// JN:今年来 LN:成立来
		Title string `json:"title"`
		// 收益率
		Syl interface{} `json:"syl"`
		// 涨跌幅
		Avg interface{} `json:"avg"`
		// 同类平均
		Hs300 interface{} `json:"hs300"`
		// 同类排名
		Rank interface{} `json:"rank"`
		// 排名总数
		Sc   interface{} `json:"sc"`
		Diff string      `json:"diff"`
	} `json:"Datas"`
}

// JJJLNEW 基金经理。。
type JJJLNEW struct {
	Datas []struct {
		Manger []struct {
			Mgrid string `json:"MGRID"`
			// 基金经理名字
			Mgrname     string `json:"MGRNAME"`
			Newphotourl string `json:"NEWPHOTOURL"`
			Isinoffice  string `json:"ISINOFFICE"`
			// 年均回报（%）
			Yieldse interface{} `json:"YIELDSE"`
			// 从业天数
			Totaldays interface{} `json:"TOTALDAYS"`
			// 任职该基金天数
			Days interface{} `json:"DAYS"`
			// 任职该基金开始时间
			Fempdate string `json:"FEMPDATE"`
			Lempdate string `json:"LEMPDATE"`
			// 任职回报（%）
			Penavgrowth     interface{} `json:"PENAVGROWTH"`
			Investmentidear string      `json:"INVESTMENTIDEAR"`
			// 金牛奖获奖次数
			HjJn interface{} `json:"HJ_JN"`
		} `json:"MANGER"`
	} `json:"Datas"`
}

// JJGM 基金规模
type JJGM struct {
	Datas []struct {
		// 日期
		Fsrq string `json:"FSRQ"`
		// 净资产（元）
		Netnav interface{} `json:"NETNAV"`
		// 净资产变动率（%）
		Change string `json:"CHANGE"`
		Issum  string `json:"ISSUM"`
	} `json:"Datas"`
}

// FHSP 分红送配
type FHSP struct {
	Datas struct {
		Fhinfo []struct {
			Fsrq string `json:"FSRQ"`
			// 权益登记日
			Djr string `json:"DJR"`
			// 每份分红（元）
			Fhfcz  interface{} `json:"FHFCZ"`
			Cfbl   string      `json:"CFBL"`
			Fhfcbz string      `json:"FHFCBZ"`
			Cflx   string      `json:"CFLX"`
			// 分红发放日
			Ffr   string `json:"FFR"`
			Fh    string `json:"FH"`
			Dtype string `json:"DTYPE"`
		} `json:"FHINFO"`
		Fcinfo []interface{} `json:"FCINFO"`
	} `json:"Datas"`
}

// JJCC 基金持仓
type JJCC struct {
	Datas struct {
		InverstPosition struct {
			// 重仓股票
			FundStocks []struct {
				// 股票代码
				Gpdm string `json:"GPDM"`
				// 股票名称
				Gpjc string `json:"GPJC"`
				// 持仓占比(%)
				Jzbl      interface{} `json:"JZBL"`
				Texch     string      `json:"TEXCH"`
				Isinvisbl string      `json:"ISINVISBL"`
				// 增持｜减持｜新增
				Pctnvchgtype string `json:"PCTNVCHGTYPE"`
				// 较上期增减比例（%）
				Pctnvchg  interface{} `json:"PCTNVCHG"`
				Newtexch  string      `json:"NEWTEXCH"`
				Indexcode string      `json:"INDEXCODE"`
				// 股票行业
				Indexname string `json:"INDEXNAME"`
			} `json:"fundStocks"`
			// 重仓债券
			Fundboods []struct {
				// 债券代码
				Zqdm string `json:"ZQDM"`
				// 债券名称
				Zqmc string `json:"ZQMC"`
				// 持仓占比（%）
				Zjzbl    string `json:"ZJZBL"`
				Isbroken string `json:"ISBROKEN"`
			} `json:"fundboods"`
			Fundfofs     []interface{} `json:"fundfofs"`
			Etfcode      interface{}   `json:"ETFCODE"`
			Etfshortname interface{}   `json:"ETFSHORTNAME"`
		} `json:"InverstPosition"`
		// 持仓资产比例
		// {
		//   "2021-03-31": [
		//     {
		//       "FSRQ": "日期",
		//       "GP":"股票占比（%）",
		//       "ZQ":"债券占比（%）",
		//       "HB": "现金占比（%）",
		//       "QT": "其他",
		//       "JZC": "净资产（亿）"
		//     }
		//   ]
		// }
		AssetAllocation map[string][]map[string]string `json:"AssetAllocation"`
		// 行业占比
		// {
		//   "2021-03-31": [
		//     {
		//         "HYMC": "行业名称",
		//         "SZ": "",
		//         "ZJZBL": "占比（%）",
		//         "FSRQ": "日期"
		//     }
		//   ]
		// }
		SectorAllocation map[string][]map[string]string `json:"SectorAllocation"`
	} `json:"Datas"`
}

// TSSJ 特色数据
type TSSJ struct {
	Datas struct {
		// 近1年夏普比率
		Sharp1      interface{} `json:"SHARP1"`
		Sharp1Nrank string      `json:"SHARP_1NRANK"`
		Sharp1Nfsc  string      `json:"SHARP_1NFSC"`
		// 近3年夏普比率
		Sharp3      interface{} `json:"SHARP3"`
		Sharp3Nrank string      `json:"SHARP_3NRANK"`
		Sharp3Nfsc  string      `json:"SHARP_3NFSC"`
		// 近5年夏普比率
		Sharp5      interface{} `json:"SHARP5"`
		Sharp5Nrank string      `json:"SHARP_5NRANK"`
		Sharp5Nfsc  string      `json:"SHARP_5NFSC"`
		// 近1年收益率
		Syl1N string `json:"SYL_1N"`
		// 成立来收益率
		SylLn string `json:"SYL_LN"`
		// 近1年最大回撤（%）
		Maxretra1      interface{} `json:"MAXRETRA1"`
		Maxretra1Nrank string      `json:"MAXRETRA_1NRANK"`
		Maxretra1Nfsc  string      `json:"MAXRETRA_1NFSC"`
		// 近3年最大回撤（%）
		Maxretra3      interface{} `json:"MAXRETRA3"`
		Maxretra3Nrank string      `json:"MAXRETRA_3NRANK"`
		Maxretra3Nfsc  string      `json:"MAXRETRA_3NFSC"`
		// 近5年最大回撤（%）
		Maxretra5      interface{} `json:"MAXRETRA5"`
		Maxretra5Nrank string      `json:"MAXRETRA_5NRANK"`
		Maxretra5Nfsc  string      `json:"MAXRETRA_5NFSC"`
		// 近1年波动率（%）
		Stddev1      interface{} `json:"STDDEV1"`
		Stddev1Nrank string      `json:"STDDEV_1NRANK"`
		Stddev1Nfsc  string      `json:"STDDEV_1NFSC"`
		// 近3年波动率（%）
		Stddev3      interface{} `json:"STDDEV3"`
		Stddev3Nrank string      `json:"STDDEV_3NRANK"`
		Stddev3Nfsc  string      `json:"STDDEV_3NFSC"`
		// 近5年波动率（%）
		Stddev5      interface{} `json:"STDDEV5"`
		Stddev5Nrank string      `json:"STDDEV_5NRANK"`
		Stddev5Nfsc  string      `json:"STDDEV_5NFSC"`
		// 持有1周盈利概率
		ProfitZ string `json:"PROFIT_Z"`
		// 持有1月盈利概率
		ProfitY string `json:"PROFIT_Y"`
		// 持有3月盈利概率
		Profit3Y string `json:"PROFIT_3Y"`
		// 持有6月盈利概率
		Profit6Y string `json:"PROFIT_6Y"`
		// 持有1年盈利概率
		Profit1N string `json:"PROFIT_1N"`
		// 近1月访问量
		PvY string `json:"PV_Y"`
		// 近1月定投人数
		DtcountY string `json:"DTCOUNT_Y"`
		// 加自选人数
		Ffavorcount string `json:"FFAVORCOUNT"`
		Earn1N      string `json:"EARN_1N"`
		// 用户平均持有时长（天）
		Avghold     string `json:"AVGHOLD"`
		Brokentimes string `json:"BROKENTIMES"`
		Isexchg     string `json:"ISEXCHG"`
	} `json:"Datas"`
}

// RespFundInfo QueryFundInfo 接口原始返回结构
type RespFundInfo struct {
	// 基金详情
	Jjxq    JJXQ    `json:"JJXQ"`
	Jdzf    JDZF    `json:"JDZF"`
	Jjgm    JJGM    `json:"JJGM"`
	Fhsp    FHSP    `json:"FHSP"`
	Jjcc    JJCC    `json:"JJCC"`
	Tssj    TSSJ    `json:"TSSJ"`
	Jjjlnew JJJLNEW `json:"JJJLNEW"`
}

// QueryFundInfo 查询基金详情
func (e EastMoney) QueryFundInfo(ctx context.Context, fundCode string) (*RespFundInfo, error) {
	apiurl := fmt.Sprintf("http://j5.dfcfw.com/sc/tfs/qt/v2.0.1/%v.json", fundCode)
	params := map[string]string{}
	logging.Debug(ctx, "EastMoney QueryFundInfo "+apiurl+" begin", zap.Any("params", params))
	beginTime := time.Now()
	resp := RespFundInfo{}
	apiurl, err := goutils.NewHTTPGetURLWithQueryString(ctx, apiurl, params)
	if err != nil {
		return nil, err
	}
	header := map[string]string{
		"user-agent": uarand.GetRandom(),
	}
	err = goutils.HTTPGET(ctx, e.HTTPClient, apiurl, header, &resp)
	latency := time.Now().Sub(beginTime).Milliseconds()
	logging.Debug(
		ctx,
		"EastMoney QueryFundInfo "+apiurl+" end",
		zap.Int64("latency(ms)", latency),
		// zap.Any("resp", resp),
	)
	if err != nil {
		return nil, err
	}
	if resp.Jjxq.Datas.Fcode == "" {
		err = fmt.Errorf("无法获取基金信息(%v)", fundCode)
	}
	return &resp, err
}
