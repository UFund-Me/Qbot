

import { dateFormat, roundToFix } from '../common'

// TODO: 使用 fetch-jsonp
const getJSONP = window['getJSONP']

/**
 * macd 买卖临界点
 */
interface ThresholdItem {
  /**
   * 当前波段的峰值
   */ 
  maxVal: number 
  /**
   * 临界点的 index
   */
  threshold: number 
}

export interface FundDataItem {
  date: string
  val: number
  // accumulatedVal: number
  // growthRate: number
  bonus: number
  isBonusPortion?: boolean // FHSP: "每份基金份额折算1.020420194份"

}

export interface FundJson {
  all: Record<string, FundDataItem>
  bonus: Record<string, FundDataItem>,
}

/**
 * 上证指数数据
 */
// export type ShangZhengData = Record<string, Pick< FundDataItem, 'date'|'val'>>

/**
 * 拉取数据, 260108
 */
export const getFundData = async (fundCode: string | number, size: number | [any, any]): Promise<FundJson> => {
  const page = 1
  let pageSize: number
  let startDate = '', endDate = ''
  if (Array.isArray(size)) {
    pageSize = (new Date(size[1]).getTime() - new Date(size[0]).getTime()) / 1000 / 60 / 60 / 24
    startDate = dateFormat(new Date(size[0]))
    endDate = dateFormat(new Date(size[1]))
  } else {
    pageSize = size
  }

  // const path = `http://api.fund.eastmoney.com/f10/lsjz?fundCode=${fundCode}&pageIndex=${page}&pageSize=${Math.floor(pageSize)}&startDate=${startDate}&endDate=${endDate}&_=${Date.now()}`
  const path = `http://fund.eastmoney.com/pingzhongdata/${fundCode}.js?v=${dateFormat(new Date(), 'yyyyMMddHHmmss')}`
  
  return new Promise((resolve) => {
    getJSONP(path, (resp) => {
    }, {
      onload: ()=>{
        let historyVal: any[] = window['Data_netWorthTrend'] || [] // 历史净值
        // 日期    x  date
        // 单位净值 y  val
        // 分红送配 unitMoney  bonus
        
        if(historyVal.length === 0) {
          console.error('查询基金净值失败', historyVal)
    
          throw new Error('查询基金净值失败')
        }
        console.log('hislen', historyVal.length)
        historyVal = historyVal.slice(-pageSize)
        console.log('historyVal ', historyVal)
    
        let previousItem
        /**
         * @important 基金数据必须是以时间倒序排序
         */
        const formatResult = historyVal.reverse().reduce((result, item) => {
          const curFundObj: FundDataItem = {
            date: dateFormat(item.x, 'yyyy-MM-dd') ,
            val: item.y,
            // accumulatedVal: item.LJJZ,
            // growthRate: item.JZZZL,
            bonus: item.unitMoney // 值为以下两种可能：拆分：每份基金份额折算1.018012713份； 分红：每份基金分红0.1元
          }
    
          result.all[curFundObj.date] = curFundObj
    
          if (curFundObj.bonus) {
            const matchResult = curFundObj.bonus.toString().match(/\d+.?\d+/)
            curFundObj.bonus = matchResult ? Number(matchResult[0]) : 0
    
            result.bonus[curFundObj.date] = curFundObj
    
            // 分红分为 分红派送，以及份额折算两种
            if ((item.unitMoney as string).startsWith('拆分')) {
              curFundObj.isBonusPortion = true
            }  
          }
    
          previousItem = curFundObj
    
          return result
        }, {
          bonus: {},
          all: {}
        })
        console.log('formatResult', formatResult)
        resolve(formatResult)
      }
    })

  })





}


export enum IndexFund {
  ShangZheng = '1.000001',
}

/**
 * 指数数据
 */
export interface IndexData {
  date: string
  val: number
  ema12: number
  ema26: number
  diff: number
  // ema9: number 
  dea: number // dea = ema(diff, 9)
  macd: number

  macdPosition: number // 当前 macd 百分位
  index?: number // 下标
  
  txnType?: 'buy'|'sell'
}

const EMA = (close: number, days: number, opt: {
  previousDate?: string,
  curDate: string,
  data: Record<string, IndexData>
}): number => {

  const { previousDate, curDate } = opt
  // 如果是首日上市价，那么初始 ema 为首日收盘价
  if (!previousDate) {
    return opt.data[curDate].val
  }
  const field = days === 9 ? `dea` : `ema${days}`
  const previousEMA = Number(opt.data[previousDate][field])

  return (2 * close + (days - 1) * previousEMA) / (days + 1)
}


/**
 * 计算 macd 百分位
 * @param indexData - 指数数据 
 */
const calcMacdPosition = (indexData: IndexData[])=>{
  let indexDataGroups: IndexData[][] = []
  indexData.reduce((previousItem, curItem)=>{
    const isSameSide = previousItem.macd * curItem.macd
    if(previousItem.macd === 0) {
      indexDataGroups.push([curItem])
      return curItem
    }

    if(isSameSide < 0) {
      // 不同边的 macd 时，创建一个新的 group
      indexDataGroups.push([curItem])
    } else {
      // 同一边的 macd
      indexDataGroups[indexDataGroups.length - 1].push(curItem) 
    }
    
    return curItem
  })
  
  // 第一天的 macd 是 0
  indexData[0].macdPosition = 0

  indexDataGroups.forEach((curIndexGroup)=>{
    const maxMacd = Math.max(...curIndexGroup.map(item => Math.abs(item.macd)))
    curIndexGroup.forEach(item => {
      const position = Math.abs(item.macd) / maxMacd
      item.macdPosition = roundToFix(position)
    })
  })
}

/**
 * 计算 macd 值
 * @param indexDataMap 源数据 map 值
 */
export const calcMACD = (indexDataMap: Record<string, IndexData>) => {
  const indexList = Object.values(indexDataMap)

  indexList.forEach((item, index) => {
    const curObj = item
    if (curObj.ema12 || curObj.ema12 === 0) {
      return
    }
    const previousDate = indexList[index - 1] ? indexList[index - 1].date : undefined
    curObj.ema12 = EMA(curObj.val, 12, {
      previousDate,
      curDate: curObj.date,
      data: indexDataMap
    })
    curObj.ema26 = EMA(curObj.val, 26, {
      previousDate,
      curDate: curObj.date,
      data: indexDataMap
    })

    curObj.diff = curObj.ema12 - curObj.ema26
    curObj.dea = previousDate ? EMA(curObj.diff, 9, {
      previousDate,
      curDate: curObj.date,
      data: indexDataMap
    }) : 0
    curObj.macd = 2 * (curObj.diff - curObj.dea)
  })

  calcMacdPosition(indexList)

  return indexDataMap
}

/**
 * 根据 macd 计算出交易点
 * @param indexData 指数数据
 * @param position 交易 macd 位置
 */
export const txnByMacd = (indexData: IndexData[], sellPosition: number, buyPosition: number ) =>{
  
  
  indexData[0].index = 0 

  let indexDataGroups: IndexData[][] = [[indexData[0]]]
  indexData.reduce((previousItem, curItem, curIndex)=>{
    curItem.index = curIndex
    const isSameSide = previousItem.macd * curItem.macd
     
    if(isSameSide < 0) {
      // 不同边的 macd 时，创建一个新的 group
      indexDataGroups.push([curItem])
    } else {
      // 同一边的 macd
       
      indexDataGroups[indexDataGroups.length - 1].push(curItem) 
    }
    
    return curItem
  })

  // const buy: Record<string, IndexData> = {}
  // const sell: Record<string, IndexData> = {}
  
  // 对分组后的 indexData 迭代
  indexDataGroups.forEach(curIndexList => {
    // const maxMacdIndexObj = curIndexList.find(indexObj => indexObj.macdPosition === 1)
    // if(!maxMacdIndexObj) {
    //   return 
    // }
    const isPositiveMacd = curIndexList[0].macd > 0
    // 如果是 正的 macd，但是没有 卖出macd临界点
    // 或者是 负的 macd，但是没有 买入macd临界点
    // 那么就没有必要计算 macd 临界点
    if((isPositiveMacd && !sellPosition) || (!isPositiveMacd && !buyPosition)) {
      return 
    }
     
    // TODO: 多峰谷，会有多个 buySellIndex 买卖点
    // 迭代，比较max 值，如果是小于 0.75max, 出现第一个 buySellIndex， 此后的 小于 max 值的数据不予理会
    // 若此后的macd 再次出现 大于 max 的 macd 值，更新 max 值，后面如果出现小于 0.75max, 出现第二个 buySellIndex，依次类推

    // 临界点列表
    const thresholdPoints = curIndexList.reduce<ThresholdItem[]>((result, cur)=>{
      const latestThreshold = result[result.length - 1]
      const curMacdVal = Math.abs(cur.macd)
      // 如果出现了新峰值, 
      if(
        curMacdVal >= latestThreshold.maxVal
        ) {
        // 且之前的前峰值有临界点，则添加新的买卖点
        if(latestThreshold.threshold !== -1) {
          result.push({
            maxVal: curMacdVal,
            threshold: -1
          })
        } else {
          // 否则更新峰值
          latestThreshold.maxVal = curMacdVal
        }
        
      }

      // 卖出策略
      if(isPositiveMacd 
        && curMacdVal <= latestThreshold.maxVal * sellPosition // 到达临界点百分位
        && latestThreshold.threshold === -1 // 该临界点还未赋值，还未被赋值
        ) {
        latestThreshold.threshold = cur.index!
      }
      // 买入策略
      if(
        !isPositiveMacd
        && curMacdVal <= latestThreshold.maxVal * buyPosition // 到达临界点百分位
        && latestThreshold.threshold === -1 // 该临界点还未赋值，还未被赋值
      ) {
        latestThreshold.threshold = cur.index!
      }
      

      return result
    }, [{
      maxVal: 0,
      threshold: -1
    }])

    const lastThresholdPoint = thresholdPoints[thresholdPoints.length - 1]
    // 如果该波段没有临界点，那么临界点即为 黄金/死亡交叉点
    if(lastThresholdPoint.threshold === -1) {
      lastThresholdPoint.threshold = curIndexList[curIndexList.length - 1].index! + 1
    }

    // const buySellIndex = greaterIndexList[greaterIndexList.length - 1].index! + 1
    console.log('临界点', thresholdPoints)
    thresholdPoints.forEach(item =>{
      const buySellIndex = item.threshold
      // 如果不存在
      if(!indexData[buySellIndex]) {
        return 
      }

      // 默认 greaterIndexList 是连续的，
      if(isPositiveMacd) {
        // 上涨行情， macdPosition 大于 xxx 的倒数第一个值，该值就是卖出点
        indexData[buySellIndex].txnType = 'sell'
        // sell[indexData[buySellIndex].date] = indexData[buySellIndex]

      } else {
        // 同理，在下跌行情中，macdPosition 大于 50% 的倒数第一个值，该值就是买入点
        indexData[buySellIndex].txnType = 'buy'
        // buy[indexData[buySellIndex].date] = indexData[buySellIndex]
      }
    })
  })

  // return {
  //   buy,
  //   sell
  // }
  
}



/**
 * 获取指数基金
 * */
export const getIndexFundData = async (opt: {
  code: string,
  range: [number | string, number | string]
}) => {
  // http://img1.money.126.net/data/hs/kline/day/history/2020/0000001.json
  /* 数据结构
  ["20200123",3037.95,2976.53,3045.04,2955.35,27276323400,-2.75]
  日期，今开，今日收盘价，最高，最低，成交量，跌幅
   */

  /**
   * http://60.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.399997&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=0&beg=20160205&end=20200205&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=cb30944405113958
   * 响应： "2020-02-06,7386.27,7452.25,7461.18,7302.34,1936321,14723348992.00"
   * 时间，今开，今收，最高，最低，成交量/手，成交额
   */

  // q.stock.sohu.com/hisHq?code=zs_000001&start=20130930&end=20200201&stat=1&order=D&period=d&rt=jsonp
  // ["2020-01-23", "3037.95", "2976.53", "-84.23", "-2.75%", "2955.35", "3045.04", "272763232",32749038.00]
  // 日期，今开，收盘，下跌，跌幅，最低，最高，成交量/手，成交额/万
  let [start, end] = opt.range.map(item => dateFormat(item))
  const savedData = JSON.parse(localStorage.getItem(opt.code) || '{}')
  const dateList = Object.keys(savedData)
  const [savedStart, savedEnd] = [dateList[0], dateList[dateList.length - 1]]

  // 如果之前没有该指数数据，拉取全部数据
  if (dateList.length === 0) {
    start = '19900101'
    end = dateFormat(Date.now())
  } else {
    // 增量更新时间范围的 指数数据
    if ((new Date(opt.range[0]) >= new Date(savedStart)) && (new Date(opt.range[1]) <= new Date(savedEnd))) {
      return savedData
    } else {
      if (new Date(opt.range[0]) >= new Date(savedStart)) {
        start = savedEnd
      }
      if (new Date(opt.range[1]) <= new Date(savedEnd)) {
        end = savedStart
      }
    }
  }
  return new Promise((resolve) => {
    getJSONP(`//60.push2his.eastmoney.com/api/qt/stock/kline/get?secid=${opt.code}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=0&beg=${start.replace(/-/g, '')}&end=${end.replace(/-/g, '')}&ut=fa5fd1943c7b386f172d6893dbfba10b`, (res) => {
      console.log(`指数基金 响应`, res.data.klines)
      const list = res.data.klines
      const indexFundData = list.reduce((result, cur: string) => {
        const [date, , val] = cur.split(',')
        result[date] = {
          date,
          val
        }
        return result
      }, {})


      let mergedData:Record<string, IndexData> = {
        ...savedData,
        ...indexFundData
      }
      const sortedDates = Object.keys(mergedData).sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
      
      mergedData = sortedDates.reduce((result, cur) => {
        result[cur] = mergedData[cur]
        return result
      }, {})
      console.log('sorted date', mergedData)

      calcMACD(mergedData)


      // console.log('shangZhengData with eacd', Object.values(mergedData).slice(0, 10), mergedData) 



      localStorage.setItem(opt.code, JSON.stringify(mergedData))

      const rangedData = {}
      // 开始时间提前 10 天，以免找不到数据
      const minDate = new Date(opt.range[0]).getTime() - 10 * 24 * 3600 * 1000
      
      // 过滤出时间区间内的数据 
      for(let date in mergedData) {
        if(date >= dateFormat(minDate) && date <= dateFormat(opt.range[1])) {
          rangedData[date] = mergedData[date]
        }
      }
      resolve(rangedData)
    })
  })


}

/**
 * 指数信息对象
 */
export interface SearchIndexResp {
  code: string
  name: string
  id: string
}
/**
 * 指数动态查询
 */
export const searchIndex = async (input: string): Promise<SearchIndexResp[]> => {
  // http://searchapi.eastmoney.com/api/suggest/get?cb=jQuery112408632397893769632_1580928562563&input=%E4%B8%AD%E8%AF%81%E7%99%BD%E9%85%92&type=14&token=D43BF722C8E33BDC906FB84D85E326E8&markettype=&mktnum=&jys=&classify=&securitytype=&count=5&_=1580928562702
  return new Promise((resolve) => {
    const path = `//searchapi.eastmoney.com/api/suggest/get?input=${input}&type=14&token=D43BF722C8E33BDC906FB84D85E326E8&markettype=&mktnum=&jys=&classify=&securitytype=&count=5&_=${Date.now()}`

    getJSONP(path, (resp) => {
      let data = resp.QuotationCodeTable.Data || []
      data = data.filter(item => item.Classify === 'Index')

      const result = data.map(item => {
        return {
          code: item.Code,
          name: item.Name,
          id: item.QuoteID
        }
      })

      resolve(result)
    })
  })
}

/**
 * 基金对象信息
 */
export interface FundInfo {
  code: string
  name: string
}
/**
 * 基金动态查询
 */
export const getFundInfo = async (key): Promise<FundInfo[]> => {
  return new Promise((resolve) => {
    const path = `https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=10&t=700&IsNeedBaseInfo=0&IsNeedZTInfo=0&key=${key}&_=${Date.now()}`

    getJSONP(path, (resp) => {
      const result = resp.Datas.map(item => {
        return {
          code: item.CODE,
          name: item.NAME
        }
      })

      resolve(result)
    })
  })

}
