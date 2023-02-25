import React, { Component } from 'react'
import { AmountProp } from './total-amount'
import { Chart, Axis, Tooltip, Geom, Legend } from 'bizcharts'
import { IndexData } from '@/utils/fund-stragegy/fetch-fund-data'
import { COLOR_NAME } from '@/utils/color'
import { roundToFix, dateFormat } from '@/utils/common'
import Slider from "bizcharts-plugin-slider";
import DataSet from "@antv/data-set";
import { CommonFundLine } from './common-line'


interface MacdLineProp extends Omit<AmountProp, 'data'> {
  data: IndexData[]
  title?: string
}

// type MacdLineProp = Omit<AmountProp, 'data'> & {
//   data: Record<string, IndexData>
// }
const ONE_YEAR = 365 * 24 * 3600 * 1000
export default class MacdLine extends Component<MacdLineProp> {
  ds = new DataSet({
    state: {
      start: dateFormat(Date.now() - 365 * 24 * 3600 * 1000),
      end: dateFormat(Date.now())
    }
  });

  getDataList() {
    const result = this.props.data
    let min = 0, max = 0
    result.forEach(item => {
      item.val = Number(item.val)
      item.macd = roundToFix(item.macd, 2)
      item.diff = roundToFix(item.diff, 2)
      item.dea = roundToFix(item.dea, 2)
      const [curMin, curMax] = [Math.min(item.macd, item.diff, item.dea), Math.max(item.macd, item.diff, item.dea)]
      min = min < curMin ? min : curMin
      max = max > curMax ? max : curMax
    })
    return { result, min, max }
  }

  sliderTimeChange = (obj: {startText: string,endText: string})=>{
    const { startText, endText } = obj;
    this.ds.setState("start", startText);
    this.ds.setState("end", endText);
  }

  render() {
    let { textMap, commonProp, title } = this.props
    textMap = {...textMap, val: '指数' }
    const macdChartProp = {
      ...commonProp.chart,
      height: 500
    }
    const { result: data, min, max } = this.getDataList()
    console.log('macd line', data)
    const commonLineScale = {
      min,
      max
    }
    const scale = {
      date: {
        type: 'timeCat'
      },
      macd: commonLineScale,
      diff: commonLineScale,
      dea: commonLineScale,
      val: {
        alias: '指数值'
      }
    }
    const ds = this.ds
    const oneYearAgoDate = dateFormat(new Date(data[data.length - 1].date).getTime() - ONE_YEAR)
    // 默认展示最近一年的指数数据
    this.sliderTimeChange({
      startText: data[0].date > oneYearAgoDate ? data[0].date : oneYearAgoDate,
      endText: data[data.length - 1].date
    })

    // 数据格式化
    const dv = ds.createView();
    dv.source(data)
      .transform({
        // 过滤出 slider 的时间范围的数据
        type: "filter",
        callback: obj => {
          const date = obj.date;
          return date <= ds.state.end && date >= ds.state.start;
        }
      })
    
    return <div >
      <h1 className="main-title" >
        参考指数曲线与 MACD 趋势图
      </h1>
       
      {/* <CommonFundLine 
          y='val'
          data={dv as any} textMap={textMap} commonProp={commonProp} /> */}

      <Chart data={dv} scale={scale}  {...macdChartProp} >
        {/* <Legend name="val" /> */}
        <Axis name='date' />
        <Axis name='macd' />
        <Axis name="diff" visible={false} />
        <Axis name="dea" visible={false} />

        <Tooltip />
        <Geom
          type="line"
          position={'date*val'}
          color={COLOR_NAME.purple}
          size={2}
          // tooltip={this.getTooltipFormat(`${y}*name`)}
        />

        <Geom type='interval'
          color={['macd', (macd) => {
            return macd > 0 ? COLOR_NAME.red : COLOR_NAME.green
          }]}
          position='date*macd' />
        {/* <Geom type='line' position='date*diff' color={COLOR_NAME.yellow} />
        <Geom type='line' position='date*dea' color={COLOR_NAME.blue} /> */}
      </Chart>

      <div>
        <Slider
          padding={[20, 40, 20, 40]}
          width="auto"
          height={26}
          start={ds.state.start}
          end={ds.state.end}
          xAxis="date"
          yAxis="macd"
          scales={{
            time: {
              type: "timeCat",
              nice: false
            }
          }}
          data={data}
          onChange={this.sliderTimeChange}
        />
      </div>
    </div>
  }
}