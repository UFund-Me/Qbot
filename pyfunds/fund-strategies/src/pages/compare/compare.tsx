import React, {Component} from 'react'
import commonStyle from '../index.css'
import {CompareSearchForm, CompareFormObj} from './search-form'
import {CompareChart, StragegyItem} from './compare-chart'
import App from '../index'
import { allSavedCondition } from '../components/saved-search'
import { FundFormObj } from '../components/search-form'
import { InvestmentStrategy, InvestDateSnapshot } from '@/utils/fund-stragegy'
import { roundToFix } from '@/utils/common'





export type ChartSnapshot = Pick<InvestDateSnapshot,'totalAmount'|'leftAmount'|'date'|'profit'|'profitRate'|'fundAmount'|'fundGrowthRate'|'dateBuyAmount'|'dateSellAmount'|'accumulatedProfit'|'maxPrincipal'|'totalProfitRate'> & {
  fundVal: number,
  position?: number, // 仓位
  txnType?: 'buy' | 'sell' | 'fixedBuy' // 当日交易类型
  origin: InvestDateSnapshot
  name?: string // 曲线名
} 



export default class CompareStragegyChart extends Component<{}, CompareStragegyChart['state']> {

  state = {
    stragegyData: [] as StragegyItem[],
    chartList: [] as string[]
  }

  handleSearch = async (formObj: CompareFormObj)=>{
    
    const app = new App({})
    const allChartPromi = formObj.stragegyChecked.map(async k => {
      const curCondition:FundFormObj = {
        ...allSavedCondition[k],
        dateRange: formObj.dateRange
      }
      const invest = await app.getFundData(curCondition)
      const investmentData: ChartSnapshot[] = invest.data.map(item => {
        return {
          name: k,
          origin: item,
          totalAmount: item.totalAmount,
          leftAmount: item.leftAmount,
          date: item.date,
          profit: item.profit,
          profitRate: item.profitRate,
          fundAmount: item.fundAmount,
          fundVal: Number(item.curFund.val),
          fundGrowthRate: item.fundGrowthRate,
          dateBuyAmount: item.dateBuyAmount,
          dateSellAmount: item.dateSellAmount,
          accumulatedProfit: item.accumulatedProfit,
          maxPrincipal: item.maxPrincipal,
          totalProfitRate: item.totalProfitRate,
          position: roundToFix(item.fundAmount / item.totalAmount, 4) 
        } as ChartSnapshot
      })
      
      return {
        name: k,
        data: investmentData 
      }
    })

    const allChartData = await Promise.all(allChartPromi)
    
    this.setState({
      stragegyData: allChartData,
      chartList: formObj.chartChecked
    })
  }

  render() {
    const {stragegyData, chartList} = this.state
    return <div className={commonStyle.normal}>
      <CompareSearchForm onSearch={this.handleSearch} />
      <CompareChart data={stragegyData} chartList={chartList} />
    </div>
  }
}