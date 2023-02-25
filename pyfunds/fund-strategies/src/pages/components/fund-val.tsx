import { Component } from "react";
import { AmountProp } from './total-amount';

import {
  G2,
  Chart,
  Geom,
  Axis,
  Tooltip,
  Coord,
  Label,
  Legend,
  View,
  Guide,
  Shape,
  Facet,
  Util,
  ChartProps
} from "bizcharts";
import React from 'react';
import { COLOR_PLATE_16, COLOR_PLATE_8, COLOR_NAME } from '@/utils/color';
import { roundToFix } from '@/utils/common';

export class FundValChart extends Component<AmountProp> {
  getTooltipFormat(text: string) {
    if(text === 'totalProfitRate*accumulatedProfit') {
      return [text, (totalProfitRate: any, accumulatedProfit: number) => ({
        name: '累计收益率',
        value: roundToFix(totalProfitRate * 100, 2)  + '%' + `(${accumulatedProfit}元)`
      })] as [string, any]
    }
    if(text === 'profitRate*profit') {
      return [text, (profitRate: any, profit: number) => ({
        name: '持有收益',
        value: roundToFix(profitRate * 100, 2)  + '%' + `(${profit}元)`
      })] as [string, any]
    }
    return [text, (fundGrowthRate, dateBuyAmount, dateSellAmount) => {
      const buyTip =dateBuyAmount ? `(${this.props.textMap['dateBuyAmount']} ${dateBuyAmount})` : ''
      const sellTip =dateSellAmount ? `(${this.props.textMap['dateSellAmount']} ${dateSellAmount})` : ''
      return {
        name: this.props.textMap['fundGrowthRate'] ,
        value: roundToFix(fundGrowthRate * 100, 2)  + '%' + buyTip + sellTip,
      }
    }] as [string, any]
  }

  xy = {
    x: 'date',
    y: 'fundGrowthRate'
  }

  /** 
   * 获取曲线最大最小值
   * */
  get scale() {
    const list = this.props.data.reduce((valList,cur)=>{
      valList.push(cur.profitRate, cur.fundGrowthRate, cur.totalProfitRate) 
      return valList
    }, [] as number[])

    const minMax = {
      min: Math.min(...list),
      max: Math.max(...list)
    }
    return {
      profitRate: minMax,
      fundGrowthRate: minMax,
      totalProfitRate: minMax
    }
  }

  render() {
    const { data, textMap, commonProp } = this.props
    const commonChartProp = commonProp.chart
    const { x, y } = this.xy
    const scale = this.scale
    const len = data.length
    const annualizedRate = len > 0 ? data[0].origin!.fundStrategy.annualizedRate : {
        fundGrowth: 0,
        totalProfit: 0
    }
    const pointColorMap = {
      // 'none': '#fff',
      'fixedBuy': COLOR_NAME.red,
      'buy': COLOR_NAME.purple,
      'sell': COLOR_NAME.green
    }

    

    return <div >
      <h1 className="main-title" >
        基金业绩走势
      </h1>

      <h2 className="sub-title">
        <span>基金收益率：{roundToFix(data[len-1].fundGrowthRate * 100, 2)}%，年化收益率：{roundToFix( annualizedRate.fundGrowth * 100,2)}%</span> <br />
        <span>定投累计收益率：{roundToFix(data[len-1].totalProfitRate * 100, 2)}%，年化收益率：{roundToFix( annualizedRate.totalProfit * 100, 2)}%</span> 
      </h2>
      
      <Chart data={data} scale={scale}  {...commonChartProp} >
        
        <Legend
          name="txnType"
          itemFormatter={val => {
              return textMap[val]
            }
          }
        />

        <Axis name={x} />
        <Axis name="fundGrowthRate" />
        <Axis name="profitRate" visible={false} />
        <Axis name="totalProfitRate" visible={false} />

        <Tooltip
          crosshairs={{
            type: "y"
          }}
        />
        <Geom
          type="line"
          position={`${x}*${y}`}
          size={2}
          color={COLOR_PLATE_16[0]}
          tooltip={this.getTooltipFormat('fundGrowthRate*dateBuyAmount*dateSellAmount')}
        />

        <Geom
          type="line"
          position="date*profitRate"
          size={2}
          color={COLOR_PLATE_16[2]}
          tooltip={this.getTooltipFormat('profitRate*profit')}
        />

        <Geom
          type="line"
          position="date*totalProfitRate"
          size={2}
          color={COLOR_PLATE_16[3]}
          tooltip={this.getTooltipFormat('totalProfitRate*accumulatedProfit')}
        />

        <Geom
          type="point"
          position={`${x}*${y}`}
          size={4}
          shape={"circle"}
          color={["txnType", (type)=>{
            return pointColorMap[type]
          }]}
          opacity={['dateBuyAmount*dateSellAmount', (...arg) => {
            const dateBuyAmount = arg[0],
            dateSellAmount = (arg as any)[1]

            if (dateBuyAmount === 0 && dateSellAmount === 0) {
              return 0
            }
            return 1
          }]}
          tooltip={this.getTooltipFormat(y + '*dateBuyAmount')}
          style={{
            lineWidth: 2,
            stroke: "#fff"
          }}
        />
      </Chart>
    </div>
  }
}