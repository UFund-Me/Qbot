import React, { Component } from 'react'
import { AmountProp } from './total-amount'
import Slider from "bizcharts-plugin-slider";
import DataSet from "@antv/data-set";
import { dateFormat } from '@/utils/common';


export interface SliderChartProp {
  y: string
  data: any[]
}

export class SliderChart extends Component<SliderChartProp> {

  ds = new DataSet({
    state: {
      start: dateFormat(Date.now() - 365 * 24 * 3600 * 1000),
      end: dateFormat(Date.now())
    }
  });

  sliderTimeChange = (obj: {startText: string,endText: string})=>{
    const { startText, endText } = obj;
    this.ds.setState("start", startText);
    this.ds.setState("end", endText);
  }
  
  render() {
    let { children, ...chartProp } = this.props
    let {data, y} = chartProp
    if(!(data && data[0])) {
      return null
    }
    
    const ds = this.ds
    this.sliderTimeChange({
      startText: data[0].date,
      endText:  data[data.length - 1].date
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

    data = dv
    const childrenWithProps = React.Children.map(this.props.children,
      (child) => React.cloneElement(child as any, {
        ...chartProp,
        data
      } ));

    return <div>
      {childrenWithProps}
      <div>
        <Slider
          padding={[20, 40, 20, 40]}
          width="auto"
          height={26}
          start={ds.state.start}
          end={ds.state.end}
          xAxis="date"
          yAxis={y}
          scales={{
            time: {
              type: "timeCat",
            }
          }}
          data={data}
          onChange={this.sliderTimeChange}
        />
      </div>
    </div>
  }
}