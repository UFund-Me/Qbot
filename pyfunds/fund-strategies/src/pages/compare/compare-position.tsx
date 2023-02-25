/**
 * 仓位比较柱状图
 */

import React, {Component} from 'react'
import { Chart, Axis, Geom, Legend, Tooltip } from 'bizcharts'
import { CommonFundLineProp } from '../components/common-line'
import DataSet from "@antv/data-set";
export interface CompareChartDataItem {
  name: string
  avgPos: number
  maxPos: number
  profitPerInvest: number
  /**
   * 累计收益/最高仓位
   */
  profitAmountPerPos: number
}

interface ComparePositionProp extends Omit<CommonFundLineProp, 'data'|'y'> {
  data: CompareChartDataItem[]
}


export class ComparePosition extends Component<ComparePositionProp> {
  render() {
    const { title,subTitle,  data, textMap, commonProp, legendProp } = this.props
    const commonChartProp = commonProp.chart 

    const ds = new DataSet();
    console.log('仓位对比数据', data)
    const dv = ds.createView().source(data);
    dv.transform({
      type: "fold",
      fields: ["avgPos", "maxPos"], // 策略名
      // 展开字段集
      key: "type",
      // key字段
      value: "value" // value字段
    });
    const scale = {
      avgPos: {
        alias: `平均仓位`
      },
      maxPos: {
        alias: `最大仓位`
      }
    }

    return <div>
    <h1 className="main-title" >
        投资策略 平均仓位与最大仓位
      </h1>
    <Chart data={dv}  {...commonChartProp} forceFit scale={scale} >
        <Legend
          itemFormatter={val => {
            return textMap[val]
          }}
         />
        <Axis name="name" />
        <Axis name="value"  />
        <Tooltip />
        {/* 平均仓位 */}
        {/* <Axis name="avgPos" />  */}
        {/* 最大仓位 */}
        {/* <Axis name="maxPos" /> */}
        {/* 收益/仓位 比 */}
        {/* <Axis name="profitOfPos" /> */}

        <Geom type="interval" color={"type"} position="name*value" adjust={[
              {
                type: "dodge",
                marginRatio: 1 / 32
              }
            ]} />
    </Chart>

    <h1 className="main-title" >
        收益/平均仓位比
    </h1>
    <Chart data={data}  {...commonChartProp} forceFit scale={scale} >
         
        <Axis name="name" />
        <Axis name="profitPerInvest"  />
        <Tooltip />

        <Geom type="interval"  position="name*profitPerInvest"   />
    </Chart>

    <h1 className="main-title" >
        累计收益/最高仓位
    </h1>
    <Chart data={data}  {...commonChartProp} forceFit scale={scale} >
         
        <Axis name="name" />
        <Axis name="profitAmountPerPos"  />
        <Tooltip />

        <Geom type="interval"  position="name*profitAmountPerPos"   />
    </Chart>
    </div>
  }
}