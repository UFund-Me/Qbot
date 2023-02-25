import React, { Component } from 'react';
import styles from './index.css';
import { FundChart } from './components/fund-line'
import { SearchForm, FundFormObj } from './components/search-form'
import 'antd/dist/antd.css'
import { getFundData, FundJson, getIndexFundData, IndexFund, calcMACD, IndexData, txnByMacd } from '@/utils/fund-stragegy/fetch-fund-data';
import { InvestmentStrategy, InvestDateSnapshot } from '@/utils/fund-stragegy';
import  notification  from 'antd/es/notification';
import moment from 'moment'
// 动态查询实时上证指数数据
// import shangZhengData from '../utils/fund-stragegy/static/shanghai.json'
import { dateFormat, roundToFix } from '@/utils/common';



export default class App extends Component<{}, {fundData: InvestDateSnapshot[]}> {
  
  state = {
    fundData: [] as InvestDateSnapshot[]
  }


  /**
   * 基金数据查询
   */
  getFundData = async (formData: FundFormObj) => {
    console.log('基金表单参数', formData)
    formData.referIndex = formData.referIndex || IndexFund.ShangZheng

    const [result, szData, referIndexData] = await Promise.all([
      getFundData(formData.fundId, formData.dateRange),
      getIndexFundData({
        code: IndexFund.ShangZheng,
        range: formData.dateRange
      }),
      formData.referIndex ? getIndexFundData({
        code: formData.referIndex,
        range: formData.dateRange
      }) : Promise.resolve(null)
    ]) 

    txnByMacd(Object.values(referIndexData), formData.sellMacdPoint/100, formData.buyMacdPoint / 100)


    const startDate = new Date( Object.keys(result.all).pop()! )
    if(startDate.getTime() > new Date(formData.dateRange[0]).getTime()) {
      formData.dateRange[0] = moment(startDate)
    }
    try {
      return this.createInvestStragegy(result, formData, {
        szData,
        indexData: referIndexData 
      })
    } catch(e) {
      notification.error({
        message: '基金创建错误',
        description: e.message
      })
      throw new Error(e)
    }
  }

  /**
   * 创建投资策略对象
   * @param fundData 基金源数据
   * @param formData 基金表单自定义选项
   */
  createInvestStragegy(fundData: FundJson, formData: FundFormObj, opt: {
    szData: Record<string, IndexData>,
    indexData: Record<string, IndexData>
  }) {


    const investment = new InvestmentStrategy({
      totalAmount: formData.totalAmount + formData.purchasedFundAmount,
      salary: formData.salary,
      shangZhengData: opt.szData,
      indexData: opt.indexData,
      
      // buyFeeRate: 0.0015,
      // sellFeeRate: 0.005,
      stop: {
        rate: 0.05,
        minAmount: 50000,
      },
    
      tInvest: {
        rate: 0.05,
        amount: 1000
      },
      fundJson: fundData,
      // 每日自定义交易操作
      onEachDay(this: InvestmentStrategy, curDate: number){
        const dateStr  = dateFormat(curDate)
        // 当前的基金快照
        const latestInvestment = this.latestInvestment
        // console.log('this day', dateFormat(curDate), this.annualizedRate.totalProfit)
        // 当日上证指数数据
        const curSzIndex = this.getFundByDate(dateStr, {
          origin: opt.szData
        })
        

        // 仓位
        const level =  roundToFix(latestInvestment.fundAmount / latestInvestment.totalAmount, 2)
        
        const curReferIndex = (opt.indexData[dateStr] || {}) as any as IndexData

        
        // PS: 此处是否收益新高，与是否 macd 卖出点 两个条件不能共存，
        // 因为一般来说，macdPosition === 1 即是收益新高
        if(
          level > formData.fundPosition/100 // 仓位大于
          && curSzIndex.val > formData.shCompositeIndex // 上证指数大于 3000
          && (!formData.sellAtTop || latestInvestment.maxAccumulatedProfit.date === latestInvestment.date)  // 是否是新高收益
          && (!formData.sellMacdPoint || curReferIndex.txnType === 'sell') // 是否是 macd 卖出点
          && latestInvestment.profitRate > (formData.profitRate/100 || -100) // 持有收益率
        ) {
          // console.log('止盈点', dateStr)
          // 止盈点减仓 10%持有 / 定值
          const sellAmount = formData.sellUnit === 'amount' ? formData.sellNum : (formData.sellNum / 100 * latestInvestment.fundAmount ).toFixed(2)
          
          this.sell(Number(sellAmount), dateStr)
        }

        

        if(
          (formData.buyMacdPoint && curReferIndex.txnType === 'buy') // 是否是 macd 买入点
        ) {
          // 补仓金额, 如果 formData.buyAmountPercent 数字小于 100，数字代表 比例，否则代表 金额
          const buyAmount = formData.buyAmountPercent <= 100 ? Math.round(latestInvestment.leftAmount * formData.buyAmountPercent / 100) : formData.buyAmountPercent
          // console.log('补仓点', dateStr, buyAmount) 
          this.buy(buyAmount, dateStr)
         
        }

         
      }
    })
    
    // investment
    //   .buy(0, '2018-12-26')
    //   .buy(5000, '2018-12-27')
    //   .sell('all', '2019-03-01')
    //   .buy(5000, '2019-08-01')
    //   .sell(2000, '2019-09-01')
    //   .buy(5000, '2019-12-01')
    investment
    .buy(formData.purchasedFundAmount, formData.dateRange[0])
    .fixedInvest({
      fixedInvestment: {
        period: formData.period[0],
        amount: formData.fixedAmount,
        dateOrWeek: formData.period[1]
      },
      range: [dateFormat(formData.dateRange[0]), dateFormat(formData.dateRange[1])]
    })
    console.log('investment', investment)
    
    this.setState({
      fundData: investment.data
    })
    return investment
  }
  
  render() {


    return (
      <div className={styles.normal}>
          <SearchForm onSearch={this.getFundData} />
          {this.state.fundData.length === 0 ? '' : <FundChart data={this.state.fundData} />}
      </div>
    );
  }
}

 