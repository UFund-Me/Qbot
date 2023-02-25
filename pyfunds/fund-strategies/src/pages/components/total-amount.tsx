import { Component } from "react";

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
import { COLOR_PLATE_8 } from '@/utils/color';
import { ChartSnapshot } from '../compare/compare';


export interface AmountProp {
  data: ChartSnapshot[]
  textMap: Record<string, string>

  commonProp: {
    chart: {
      forceFit: ChartProps['forceFit']
      height: ChartProps['height']
      padding: ChartProps['padding']
    }
  }

  legendProp?: {
    attachLast: boolean
  }
}

export interface AmountState {

}
 

export class TotalAmountChart extends Component<AmountProp> {
 

  getTooltipFormat(text: string) {
    return [text, (value: any) => ({
      name: this.props.textMap[text],
      value,
    })] as [string, any]
  }

  /** 
   * 获取曲线最大最小值
   * */
  get scale() {
    const list = this.props.data.reduce((valList,cur)=>{
      valList.push(cur.totalAmount, cur.leftAmount, cur.fundAmount) 
      return valList
    }, [] as number[])

    const minMax = {
      min: Math.min(...list),
      max: Math.max(...list)
    }
    return {
      totalAmount: minMax,
      leftAmount: minMax,
      fundAmount: minMax
    }
  }

  render() {
    const { data, textMap, commonProp } = this.props
    const commonChartProp = commonProp.chart
    const scale = this.scale
    return <div >
      <h1 className="main-title" >
        资产增长趋势图
      </h1>
      {/* <h2 className="sub-title"  >
        设置左右刻度数tickCount相同
      </h2> */}
      <Chart  data={data} scale={scale} {...commonChartProp} >
        <Legend
          itemFormatter={val => {
            return textMap[val]
          }}
        />
        <Axis name="date" />
        <Axis name="totalAmount" />
        <Axis name="leftAmount" visible={false} />
        <Axis name="fundAmount" visible={false} />

        <Tooltip
          crosshairs={{
            type: "y"
          }}
        />
        <Geom
          type="line"
          position="date*totalAmount"
          size={2}
          color={COLOR_PLATE_8[0]}
          tooltip={this.getTooltipFormat('totalAmount')}
        />
        <Geom
          type="line"
          position="date*leftAmount"
          size={2}
          color={COLOR_PLATE_8[1]}
          tooltip={this.getTooltipFormat('leftAmount')}
        />
        <Geom
          type="line"
          position="date*fundAmount"
          size={2}
          color={COLOR_PLATE_8[7]}
          tooltip={this.getTooltipFormat('fundAmount')}
        />
{/* 
        <Geom
          type="line"
          position="date*maxPrincipal"
          size={2}
          color={COLOR_PLATE_8[5]}
          tooltip={this.getTooltipFormat('maxPrincipal')}
        /> */}
        {/* <Geom
          type="point"
          position="date*totalAmount"
          size={2}
          shape={"circle"}
          style={{
            stroke: "#fff",
            lineWidth: 1
          }} 
        />*/}
      </Chart>
    </div>
  }
}
