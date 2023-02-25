 /**************************
 * 投资类 描述了 指定策略下的投资过程
 * 投资快照类 描述了投资过程中，某一天的状态
 **************************/

import { FundJson } from "../../../tools/get-fund-data-json"
import { dateFormat, roundToFix } from "../common"
import { FundDataItem, IndexData } from './fetch-fund-data'
// import FundDataJson from './static/景顺长城新兴成长混合260108.json'
const ONE_DAY = 24 * 60 * 60 * 1000

interface FundTransaction {
  /** 
   * 份额 
   * */
  portion: number 
  /** 
   * 基金净值
   * */
  val: number 
  /** 
   * 金额
   * */
  amount: number
}

export interface FixedInvestOption {
  fixedInvestment: {
    amount: number // 每次定投金额
    dateOrWeek: number // 每周周几，每月几号定投
    period: 'weekly' | 'monthly'   // 每周，每月，每 2 周定投
  }, 
  range: [string| Date, string| Date]
}

export class InvestmentStrategy {
  totalAmount!: number // 初始资本，存量
  salary!: number // 工资，每月增量资金

  /**
   * 定投时，每一天的回调函数
   */
  onEachDay!: Function

  
  /**
   * 当前投资的状态
   */
  latestInvestment!: InvestDateSnapshot

  /**
   * (上证)指数数据
   */
  shangZhengData!: Record<string, IndexData> 

  /**
   * 跟踪指数指标
   */
  indexData?: Record<string, IndexData> 
  fundJson!: FundJson // 基金源数据
  
  buyFeeRate: number = 0.0015 // 买入的手续费， 一般是 0.15%
  sellFeeRate: number = 0.005 // 卖出的手续费， 一般是 0.5%
  
  // 止盈点， 
  stop!: {
    rate: number  // 基金涨了 5 % 就止盈一部分
    minAmount: number // 止盈的最低 持仓临界线，如低于 10% 
  }

  // 做 T 时的配置信息
  tInvest!: {
    rate: number // 自上次止盈后， 降幅 rate 幅度后 做 T
    amount: number // 补仓 份额 （买）
  }

  /**
   * 该基金策略下运行的每个交易日的数据
   */
  data: InvestDateSnapshot[] = []
  /**
   * 标识日期-数据
   */
  dataMap: Record<string, InvestDateSnapshot> = {}

  /**
   * 定投配置
   */
  fixedConfig!: FixedInvestOption

  /**
   * 年化收益率
   * - 基金折合年化收益率
   * - 累计年化收益率
   */
  get annualizedRate():{
    fundGrowth: number
    totalProfit: number
  } {
    const len = this.data.length
    if(len > 0) {
      const startFund = this.data[0]
      const endFund = this.data[len - 1]
      const rangeTime = new Date(endFund.date).getTime() - new Date(startFund.date).getTime()
      const rangeYear = rangeTime / ONE_DAY / 365
      
      return {
        fundGrowth: roundToFix(Math.pow( 1 + endFund.fundGrowthRate, 1 / rangeYear ) - 1 , 4) ,
        totalProfit:roundToFix( Math.pow( 1 + endFund.totalProfitRate, 1 / rangeYear ) - 1, 4) ,
      }
    } else {
      return {
        fundGrowth: 0,
        totalProfit: 0
      }
    }
  }

  /**
   * 基金的长期投资计划
   */
  constructor(options: Pick<InvestmentStrategy, 'fundJson'|'salary'|'stop'|'tInvest'|'totalAmount'|'indexData'|'shangZhengData'|'onEachDay'>) {
    Object.assign(this, options)
  }

  /** 
   * 是否应该定投
   */
  private shouldFixedInvest(fixedInvestment: FixedInvestOption['fixedInvestment'], date:any):boolean {
    const now = new Date(date)
    if(fixedInvestment.period === 'monthly') {
      return now.getDate() === fixedInvestment.dateOrWeek
    } else if(fixedInvestment.period === 'weekly') {
      return now.getDay() === fixedInvestment.dateOrWeek
    } else {
      return false 
    }
  }

  /**
   * 策略定投
   */
  fixedInvest(opt: FixedInvestOption) {
    const {range, fixedInvestment} = opt
    this.fixedConfig = opt
    
    // 定投策略
    const beginTime = new Date(range[0]).getTime()
    const endTime = new Date(range[1]).getTime()
    if(beginTime > endTime){
      throw new Error('range[1] should not less than range[0]')
    }
    let curDate = beginTime // 中间的日期

    while(curDate <= endTime) {
      // 如果还没有数据, 填充初始数据
      // if(!this.data || this.data.length === 0) {
      //   this.buy(0, curDate - ONE_DAY)
      // }  

      if(this.shouldFixedInvest(fixedInvestment, curDate)){
        this.buy(fixedInvestment.amount, curDate)
      } else {
        this.buy(0, curDate)
      }

      this.onEachDay(curDate)
      
      curDate += 24 * 60 * 60 * 1000
    }

    return this
  }

  /** 
   * 获取指定日期的基金快照
   */
  private getSnapshotInstance(date:any):InvestDateSnapshot {
    if(this.dataMap[date]) {
      return this.dataMap[date]
    } else {
      return new InvestDateSnapshot({
        fundStrategy: this,
        date: date
      })
    }
  }

  /**
   * 数据更新
   */
  private pushData(investSnap: InvestDateSnapshot) {
    this.data.push(investSnap)
    // 标识 该日期是否已存在实例
    if(!this.dataMap[investSnap.date]) {
      this.dataMap[investSnap.date] = investSnap
    }
  }


  /**
   * 买入基金
   */
  buy(amount: number, date: any) {
    const dateStr = dateFormat(date)
    let cur = new Date(date).getTime()

    // 填充起始时间和 终止时间之间的空白数据
    if(this.latestInvestment) {
      let latestInvestDate = new Date(this.latestInvestment.date).getTime()
      latestInvestDate += ONE_DAY
      while(cur > latestInvestDate) {
        
        const invest = this.getSnapshotInstance(latestInvestDate).buy(0)
        // console.log('date', invest.date, invest)
        this.pushData(invest)
        latestInvestDate += ONE_DAY
      }
    }  
    const invest = this.getSnapshotInstance(dateStr).buy(amount)

    this.pushData(invest)
    return this
  }

  /**
   * 赎回基金
   * @param amount 赎回金额
   * @param date 日期
   */
  sell(amount:number|'all', date: any) {
    const dateStr = dateFormat(date)
    let cur = new Date(date).getTime()

    // 填充起始时间和 终止时间之间的空白数据
    if(this.latestInvestment) {
      let latestInvestDate = new Date(this.latestInvestment.date).getTime()
      latestInvestDate += ONE_DAY
      while(cur > latestInvestDate) {
        const invest = this.getSnapshotInstance(latestInvestDate).sell({amount: 0})
        this.pushData(invest)
        latestInvestDate += ONE_DAY
      }
    }  
    const invest = this.getSnapshotInstance(dateStr)
    if(amount === 'all') {
      invest.sell('all')
    } else {
      invest.sell({amount})
    }

    this.pushData(invest)
    return this
  }

  /**
   * 根据日期获取对应的基金信息
   */
  getFundByDate(date: string, opt?: {
    origin: Record<string , any>
  }): FundDataItem {
    let originData = this.fundJson.all
    if(opt && opt.origin) {
      originData = opt.origin
    }
    const result = originData[  date ]
    // 如果没有 result， 说明那一天是 非交易日，往更早的日期取值
    if(!result) {
      const previewValidDate = dateFormat( new Date(date).getTime() - 24 * 60 * 60 * 1000)
      return this.getFundByDate(previewValidDate, opt)
    } else {
      return result
    }
    
  }
}

/**
 * 投资周期中，某一天的持仓快照
 */
export class InvestDateSnapshot {
  // 基础数据： cost， portion，totalBuyAmount，totalSellAmount，maxPrincipal，leftAmount，date，curFund，curBonus，dateBuyAmount，dateSellAmount
  /**
   * 基金投资策略
   */
  fundStrategy: InvestmentStrategy 

  /** 
   * 持仓成本 单价，已经包含了 买入费率 的成本了
   * */ 
  cost!: number // 每天操作后计算赋值
   

  /**
   * 持仓成本金额, 已经包括了买入费率，手续费也是自己的成本
   */
  get costAmount():number {
    return roundToFix( this.cost * this.portion , 2 )
  }

  /** 
   * 持仓份额  
   * */
  portion!:number // 每天操作后计算赋值
   

  /**
   * 持仓金额 = 当前净值 * 持有份额
   */
  get fundAmount():number {
    return roundToFix( this.curFund.val * this.portion, 2)
  } 

  /** 
   * 持有收益 = （当前净值 - 持有成本）* 持仓份额  
   * */
  get profit():number {
    return roundToFix((this.curFund.val - this.cost) * this.portion, 2)
  } 
  /** 
   * 持有收益率 = （当前净值 / 成本价）- 1 
   * 依赖 this.cost
   * */
  get profitRate():number {
    if(this.costAmount === 0) {
      return 0
    }
    return roundToFix( this.curFund.val / this.cost - 1, 4 ) 
  }
 

  /**
   * 总共买入的金额 
   */
  totalBuyAmount!: number //    * 需要手动赋值初始化

  /**
   * 总共卖出的金额 
   */
  totalSellAmount!: number // * 需要手动赋值初始化

 
  /**
   * 最大本金，累计成本， 用于算累计收益率 https://sspai.com/post/53061
   */
   maxPrincipal!:number 

  /**
   * 累计收益率
   */
  get totalProfitRate() {
    if(this.maxPrincipal === 0) {
      return 0
    }
    return roundToFix( this.accumulatedProfit / this.maxPrincipal, 4 )
  }

  /**
   * 资金弹药，还剩下多少钱可以加仓，可用资金
   * = 上一个交易日的 leftAmount + (今日加减仓)
   */
  leftAmount!:number 
  
  /**
   * 总资产 = 资金弹药 +  持仓金额
   */
  get totalAmount(): number  {
    return roundToFix( this.leftAmount + this.fundAmount , 2)
  }

  /**
   * 累计收益
   */
  get accumulatedProfit() {
    return roundToFix( this.fundAmount - this.totalBuyAmount + this.totalSellAmount, 2)
  }

  /**
   * 某个区间内累计的最大收益
   */
  maxAccumulatedProfit!: {
    date: string
    amount: number
  }


  
  date: string // 当前日期

  // get shouldFixedInvest():boolean {
  //   const now = new Date(this.date)
  //   const fixedInvestment = this.fundStrategy.fixedInvestment
  //   if(fixedInvestment.period === 'monthly') {
  //     return now.getDate() === fixedInvestment.dateOrWeek
  //   } else if(fixedInvestment.period === 'weekly') {
  //     return now.getDay() === fixedInvestment.dateOrWeek
  //   } else {
  //     return false 
  //   }
  // }

  /**
   * 当前基金数据
   */
  curFund: FundDataItem 

  /**
   * 获取区间内的分红点
   * @param start 开始时间
   * @param end 结束时间
   */
  private getBonusBetween(start, end) {
    const startDate = new Date(start).getTime(),
          endDate = new Date(end).getTime()
    const bonus = this.fundStrategy.fundJson.bonus
    
    const bonusFundList = Object.values(bonus).reduce((relatedBonus, cur)=>{
      const curDate = new Date(cur.date).getTime()
      if( curDate >= startDate && curDate <= endDate) {
        relatedBonus.push(cur)
      }
      return relatedBonus
    }, [] as FundDataItem[])
    return bonusFundList
  }

  curBonus: FundDataItem[] = []

  /**
   * 是否是分红日
   */
  get isBonus():boolean {
    return Boolean(this.fundStrategy.fundJson.bonus[this.date])
  }

  /**
   * 基金在区间内的涨幅
   */
  get fundGrowthRate():number {
    

    // 个时间点到某个时间点之间的 涨幅比较
    // 普通场景 涨幅： Tb / Ta - 1 
    // 中间存在 分红点
    // 多个分红点： 最新净值 / 开始点的净值 * 【(分红点分红后当天涨跌后净值 + 分红值) / 分红点分红后当天涨跌后净值 * (分红点2 + 分红值) / 分红点2 * ...  】  - 1 
    if(this.fundStrategy.data[0]) {
      const bonus = this.curBonus
      // 起始基金净值
      const firstFundVal = this.fundStrategy.data[0].curFund.val
      if(bonus.length === 0) {
        return roundToFix((this.curFund.val - firstFundVal) / firstFundVal, 4)
      } else {
        let growWithBonus = bonus.reduce((result, curBonus)=>{
          if(curBonus.isBonusPortion) {
            return result * curBonus.bonus
          } else {
            return result * (Number(curBonus.val) + Number(curBonus.bonus)) / curBonus.val  
          }
          
        }, this.curFund.val/firstFundVal) - 1
        return roundToFix(growWithBonus, 4)
      }
      
    } else {
      return 0
    }
  }

  /**
   * 当天买入 金额（不计手续费）
   */
  dateBuyAmount: number = 0
  /**
   * 当天卖出的金额
   */
  dateSellAmount: number = 0
  fixedBuy!: FundTransaction|null// 被动定投买入份额，金额。 金额 = 份额 * 基金净值
  profitSell!: FundTransaction|null // 被动触发条件 卖出止盈的，份额，金额，
  buyWhenDecline!: FundTransaction|null // 主动补仓买入份额，金额
  sellWhenRise!: FundTransaction|null // 卖出补仓做 T 的份额，金额，

  /**
   * @param options 
   */
  constructor(options: Partial<Pick<InvestDateSnapshot, 'date'|'fundStrategy'|'cost'|'leftAmount'|'portion'>>) {
    
    
    // 每天的操作，只需要手动更新：date, cost，portion, leftAmount
    this.date = options.date ? dateFormat(options.date) : dateFormat(Date.now())
    this.fundStrategy = options.fundStrategy!
    try {
      this.curFund = this.fundStrategy.getFundByDate(this.date)
    } catch(e) {
      throw new RangeError('所选时间超出基金运营范围')
    }
    if(!this.fundStrategy.latestInvestment) {
      this.portion = 0
      this.cost = 0
      this.totalBuyAmount = 0
      this.totalSellAmount = 0
      this.leftAmount = this.fundStrategy.totalAmount
      this.maxPrincipal = 0
    } else {
      const latestInvestment = this.fundStrategy.latestInvestment
      this.portion = latestInvestment.portion
      this.cost = latestInvestment.cost
      this.leftAmount = latestInvestment.leftAmount
      this.totalBuyAmount = latestInvestment.totalBuyAmount
      this.totalSellAmount = latestInvestment.totalSellAmount
      this.maxPrincipal = latestInvestment.maxPrincipal
      this.curBonus = this.getBonusBetween(this.fundStrategy.data[0].date, this.date)
    }

    this.operate()
    this.calcMaxAccumulatedProfit()
  }

  /**
   * 计算累计的历史最大收益
   */
  private calcMaxAccumulatedProfit() {
    const curMaxProfit = {
      date: this.date,
      amount: this.accumulatedProfit
    }
    const previousInvestment = this.fundStrategy.data[this.fundStrategy.data.length - 1] 

    if(previousInvestment && previousInvestment.maxAccumulatedProfit) {
      // 比较当前最大，和上一次比较最大值
      this.maxAccumulatedProfit = previousInvestment.maxAccumulatedProfit.amount > curMaxProfit.amount ? previousInvestment.maxAccumulatedProfit : curMaxProfit
    } else {
      // 如果是第一个值，初始化
      this.maxAccumulatedProfit = curMaxProfit
    }
  }

  /**
   * 该日期基金操作行为
   */
  private operate() {
    this.income()
    // 分红日？重新计算 成本和 份额。【分红后，收益不变，净值变低。 所以 持仓成本 = 分红后净值/ （profitRate+1）】【份额 = fundAmount / 分红后净值】
    if(this.isBonus) {
      if(this.curFund.isBonusPortion) {
        this.cost = this.cost / this.curFund.bonus
        this.portion = this.portion * this.curFund.bonus
      } else {
        this.cost = this.cost * this.curFund.val / (Number(this.curFund.val) + Number(this.curFund.bonus)) 
        this.portion = this.portion * (Number(this.curFund.val) + Number(this.curFund.bonus)) / this.curFund.val
      }
      
    }
    // 定投日? 买入定投金额
    // if(this.shouldFixedInvest) {
    //   this.buy(this.fundStrategy.fixedInvestment.amount)
    // }
    
    //  触发补仓？

    //  触发止盈？

    //  触发卖出补仓份额？

    

    // 剩余资金小于 0， 即为爆仓
    // if(this.fundAmount < 0) {
  
    // }

    this.fundStrategy.latestInvestment = this
    
  }

  /**
   * 计算最大的投入本金， 参考： https://sspai.com/post/53061
   * 每次买入，都要重新 执行本方法，计算投入本金。
   * 卖出无需执行，因为maxPrincipal 只会增，不会减
   */
  private calcMaxPrincipal() {
    
    // 如果当前本金 比上一次本金 高，那么更新 最大本金
    if(this.maxPrincipal < this.costAmount) {
      this.maxPrincipal = this.costAmount
    }  
  }

  /**
   * 发工资，增加可用资金
   */
  private income() {
    // const latestInvestment = this.fundStrategy.latestInvestment
    // const latestInvestmentAmount = latestInvestment ? latestInvestment.leftAmount : 0
    const salaryDate = 1
    // 发薪日
    if(new Date(this.date).getDate() === salaryDate) {
      this.leftAmount +=  this.fundStrategy.salary
    }  
  }
  
  /**
   * 填充满买入时交易相关数据
   * @param txn 交易数据
   */
  private fulfillBuyTxn(txn:Partial<FundTransaction>): FundTransaction{
    txn.val = txn.val || this.curFund.val
    if( !isNaN(txn.amount!) && !txn.portion) {
      // 除去买入费率的 净申购金额 (参考 支付宝基金买入申购计算)
      txn.amount = roundToFix( txn.amount! / (1 + this.fundStrategy.buyFeeRate), 2 )
      txn.portion = roundToFix(txn.amount / txn.val, 2)
    }
 
    return txn as FundTransaction
  }

  /**
   * 填充满卖出时交易相关数据
   * @param txn 交易数据
   */
  private fulfillSellTxn(txn:Partial<FundTransaction>): FundTransaction{
    txn.val = txn.val || this.curFund.val
    let portion:number 
    // 卖出只能用份额计算
    // 如果是卖出 指定 amount，转换成份额
    if((txn.amount || txn.amount === 0) && !txn.portion) {
      portion = roundToFix(txn.amount / txn.val, 2)
    } else if(isNaN(txn.amount!) && txn.portion) {
      // 如果是卖出指定 份额
      portion = txn.portion
    } else {
      throw new Error('txn.portion 和 txn.amount 必须有且只有一个值')
    }
    txn.portion = portion

    // 卖出的真实 到账金额
    txn.amount = txn.val * portion * (1 - this.fundStrategy.sellFeeRate)
 
    return txn as FundTransaction
  }
 
  /**
   * 买入基金行为，买入金额
   * @param amount 金额
   */
  buy(amount:number) {
    // 分红日不允许买卖
    if(this.isBonus) {
      return this
    }
    // amount 是掏出的钱
    // buyTxn.amount 是除去 手续费后，确切买入基金的金额， 两者差价为买入手续费
    if(amount <= 0) {
      return this
    }
    this.totalBuyAmount += amount
    this.dateBuyAmount += amount

    const buyTxn = this.fulfillBuyTxn({
      amount
    })
    // 上一次快照
    // const latestInvestment = this.fundStrategy.data[this.fundStrategy.data.length - 1]  || {
    //   portion : 0,
    //   cost: 0,
    //   costAmount: 0,
    //   leftAmount: this.leftAmount
    // }

    const tempCostAmount = this.costAmount
    // 最新份额 = 上一次的 份额，加最新买入的份额
    this.portion = this.portion + buyTxn.portion

    // 买入行为后，持仓成本 = (之前持仓成本金额 + 买入金额) / 基金总份额
    this.cost = roundToFix( (tempCostAmount + amount)  / this.portion , 4)

    // 买入后从剩余资金扣除
    this.leftAmount = roundToFix(this.leftAmount - amount, 2) 
    
    this.calcMaxPrincipal()
    return this
  }
  /**
   * 卖出基金
   * @param txn 卖出信息
   */
  sell(txn:Partial<FundTransaction>|'all') {
    // 分红日不允许买卖
    if(this.isBonus) {
      return this
    }

    // 上一次快照， 
    // const latestInvestment = this.fundStrategy.data[this.fundStrategy.data.length - 1]  || {
    //   portion : 0,
    //   cost: 0,
    //   costAmount: 0,
    //   leftAmount: this.fundStrategy.totalAmount
    // }

    if(txn === 'all') {
      txn = {
        portion: this.portion
      }
    }

    if(txn && (txn.amount! <= 0 || txn.portion! <= 0)) {
      return this
    }
    const sellTxn = this.fulfillSellTxn(txn)
    // 此时的 this.fundStrategy.latestInvestment 其实就是 this, 因为 sell() 执行前， latestInvestment 就已经被赋值了
    

    if(this.portion - sellTxn.portion < 0) {
      console.error('卖出份额不能比持有份额高, 跳过本次卖出')
    }
    // 最新份额 = 上一次的 份额 - 最新卖出的份额
    this.portion = this.portion - sellTxn.portion
    

    // 卖出行为后，持仓成本 = (之前持仓成本金额 - 卖出金额) / 基金总份额
    // this.cost = (latestInvestment.costAmount - sellTxn.amount)  / this.portion
    // 算法参考 https://www.zhihu.com/question/265056524
    
    // this.returnedProfit = latestInvestment.returnedProfit +  sellTxn.amount / (1/this.profitRate + 1)

    // 卖出后加到 剩余资产中
    this.leftAmount = roundToFix( this.leftAmount + sellTxn.amount, 2 )
    
    this.totalSellAmount = roundToFix( this.totalSellAmount + sellTxn.amount, 2)
    this.dateSellAmount = roundToFix(this.dateSellAmount + sellTxn.amount, 2) 

    return this
  }

}



// 买卖
// investment
    //   .buy(0, '2018-12-26')
    //   .buy(5000, '2018-12-27')
    //   .sell('all', '2019-03-01')
    //   .buy(5000, '2019-08-01')
    //   .sell(2000, '2019-09-01')
    //   .buy(5000, '2019-12-01')
    
    // 定投
    // investment.fixedInvest({
    //   fixedInvestment: {
    //     period: 'weekly',
    //     amount: 1200,
    //     dateOrWeek: 4
    //   },
    //   range: ['2019-01-01','2019-12-01']
    // })
