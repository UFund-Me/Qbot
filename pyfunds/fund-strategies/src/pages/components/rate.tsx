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
import { COLOR_PLATE_16 } from '@/utils/color';

export class RateChart extends Component<AmountProp> {
  getTooltipFormat(text: string) {
    return [text, (value: any) => ({
      name: this.props.textMap[text],
      value,
    })] as [string, any]
  }


  render() {
    const { data, textMap, commonProp } = this.props
    const commonChartProp = commonProp.chart

    return <div >
      <h1 className="main-title" >
        累计收益趋势图
      </h1>
      {/* <h2 className="sub-title"  >
        设置左右刻度数tickCount相同
      </h2> */}
      <Chart  data={data}  {...commonChartProp} >
        <Legend
          itemFormatter={val => {
            return textMap[val]
          }}
        />
        <Axis name="date" />
        <Axis name="profitRate" />
        <Axis name="profit" />

        <Tooltip
          crosshairs={{
            type: "y"
          }}
        />
        
        {/* <Geom
          type="line"
          position="date*profitRate"
          size={2}
          color={COLOR_PLATE_16[2]}
          tooltip={this.getTooltipFormat('profitRate')}
        /> */}
         
         {/* <Geom
          type="line"
          position="date*profit"
          size={2}
          color={COLOR_PLATE_16[4]}
          tooltip={this.getTooltipFormat('profit')}
        /> */}
        <Geom
          type="line"
          position="date*accumulatedProfit"
          size={2}
          color={COLOR_PLATE_16[5]}
          tooltip={this.getTooltipFormat('accumulatedProfit')}
        />
         
      </Chart>
    </div>
  }
}