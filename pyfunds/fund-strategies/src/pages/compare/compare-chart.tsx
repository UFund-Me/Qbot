import React, {Component} from 'react'
import { AmountProp } from '../components/total-amount'
import { CommonFundLine, CommonFundLineProp } from '../components/common-line'
import { keyTextMap } from '../components/fund-line'
import {ChartSnapshot} from './compare'
import { InvestDateSnapshot } from '@/utils/fund-stragegy'
import { formatPercentVal, roundToFix } from '@/utils/common'
import { ComparePosition, CompareChartDataItem } from './compare-position'

const commonProp:AmountProp['commonProp'] = {
  chart: {
    forceFit: true,
    height: 450, 
    padding: [
      20, 80, 100, 80
    ]
  }
}

/**
 * 需要百分比展示的数据
 */
const percentProp: (keyof ChartSnapshot)[] = ['fundGrowthRate','profitRate', 'totalProfitRate', 'position']

export interface StragegyItem {
  name: string, 
  data: ChartSnapshot[] 
}

export interface CompareChartProp {
  data: StragegyItem[]
  /**
   * 需要展示的图表列表
   */
  chartList: string[]
}

export class CompareChart extends Component<CompareChartProp> {

  

  render() {
    const {data} = this.props
    if(!data || data.length === 0) {
      return null
    }
    const intervalChartData: CompareChartDataItem[] = data.map((stragegy)=>{
      let maxPos = 0
      let avgPos = stragegy.data.reduce((result, cur) => {
        const curPos = cur.position!
        maxPos = curPos > maxPos ? curPos : maxPos
        return result + curPos
      }, 0) / stragegy.data.length
      const profitPerInvest = stragegy.data[stragegy.data.length - 1].totalProfitRate / avgPos 
      const profitAmountPerPos = stragegy.data[stragegy.data.length - 1].accumulatedProfit / maxPos

      return {
        name: stragegy.name,
        avgPos: roundToFix(avgPos * 100),
        maxPos: roundToFix(maxPos * 100),
        profitPerInvest: roundToFix(profitPerInvest),
        profitAmountPerPos: roundToFix(profitAmountPerPos)
      }
    })
    const allData = data.reduce<ChartSnapshot[]>((resule, item) => {
      return [
        ...resule,
        ...item.data
      ]
    }, [])
    // const first = this.props.data[0].data
    const {chartList} = this.props
    console.log('allData', allData)

    return <div>
      {
        chartList.map((chartProp: any,index) => {
          const prop:CommonFundLineProp = {
            y: chartProp,
            data: allData,
            textMap: keyTextMap,
            commonProp,
            formatVal: percentProp.includes(chartProp) ? formatPercentVal : undefined
          }
        return <CommonFundLine  key={index} {...prop}  />
        })
      }
      <ComparePosition  
        commonProp={commonProp} 
        textMap={keyTextMap} 
        data={intervalChartData} />
    </div>
  }
}