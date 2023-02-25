import { Component } from "react";
import { AmountProp } from './total-amount';

import {
  Chart,
  Geom,
  Axis,
  Tooltip,
  Legend,
} from "bizcharts";
import React from 'react';

export interface CommonFundLineProp extends AmountProp {
  title?: string
  subTitle?: string
  /* 
   * y 轴数据属性
   */
  y: string 

  /**
   * 格式化 tooltip 数据
   */
  formatVal?: (val:any)=>any
}

export class CommonFundLine extends Component<CommonFundLineProp> {
  
  private getTooltipFormat(expr: string) {
    const {formatVal} = this.props
    const text = this.props.textMap[this.props.y]
    return [expr, (value: any, legendName: string) => ({
      name: (legendName || '') + `(${text})`,
      value: formatVal ? formatVal(value) : value,
    })] as [string, any]
  }


  render() {
    const { title,subTitle, y, data, textMap, commonProp, legendProp } = this.props
    const commonChartProp = commonProp.chart 

      return <div >
      <h1 className="main-title" >
        {title || textMap[y]}
      </h1>
      { subTitle ? <h2 className="sub-title"  >
        {subTitle}
      </h2>: ''}

      <Chart  data={data}  {...commonChartProp} scale={{
      date: {
        type: 'timeCat'
      }}} >
        <Legend
          {...(legendProp as any || {})}
        />
        <Axis name="date" /> 

        <Tooltip
          crosshairs={{
            type: "y"
          }}
        /> 
        <Geom
          type="line"
          position={'date*' + y}
          size={2}
          color="name"
          tooltip={this.getTooltipFormat(`${y}*name`)}
        />
         
      </Chart>
    </div>
  }
}