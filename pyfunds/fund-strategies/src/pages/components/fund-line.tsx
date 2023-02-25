
/* 
图表
done 1. 总资产 totalAmount  基金资产 fundAmount 3. 剩余可用资金 leftAmount 【是否爆仓】


done 4. 基金净值 fundVal + 买入红点，卖出蓝点
done 5. 收益率profitRate + 累计盈亏 profit 
done 6. 仓位 = 资金资产 / 总资产

7. 结果值：平均年化收益率， 最大回撤
*/
import React, { Component } from 'react';
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
  Util
} from "bizcharts";
import { InvestmentStrategy, InvestDateSnapshot } from '@/utils/fund-stragegy/index.ts';
import { TotalAmountChart, AmountProp } from './total-amount'
import { FundValChart } from './fund-val'
import { RateChart } from './rate'
import {CommonFundLine} from './common-line'
import { ChartSnapshot } from '../compare/compare';
import { roundToFix } from '@/utils/common';
import MacdLine from './macd';
import { SliderChart } from './slider-chart';

/**
 * 数据映射表
 */
export const keyTextMap = {
  totalAmount: '总资产',
  leftAmount: '剩余可用资金',
  profitRate: '持有收益率',
  profit: '持有收益',
  fundAmount: '基金持有金额',
  fundVal: '基金净值',
  fundGrowthRate: '基金涨幅',
  dateBuyAmount: '买入金额',
  dateSellAmount: '卖出金额',
  accumulatedProfit: '累计盈亏',
  maxPrincipal: '累计本金',
  totalProfitRate: '累计收益率',
  position: '持有仓位',
  
  buy: '买入',
  fixedBuy: '定投',
  sell: '卖出',
  avgPos: '平均仓位',
  maxPos: '最大仓位',
  profitPerInvest: '收益仓位比',
}


export class FundChart extends Component<{data: InvestDateSnapshot[]}> {

  commonProp: AmountProp['commonProp'] = {
    chart: {
      forceFit: true,
      height: 450, 
      padding: [
        20, 80, 100, 80
      ]
    }
  }

  render() {
    // 定投金额
    const fixedInvestAmount = this.props.data[0].fundStrategy.fixedConfig.fixedInvestment.amount

    const investmentData = this.props.data.map(item => {
      let txnType 
      
      if (item.dateBuyAmount > 0 ) {
        txnType = item.dateBuyAmount === fixedInvestAmount ? 'fixedBuy' : 'buy'
      } 
      if(item.dateSellAmount > 0){
        txnType = 'sell'
      }
      
      return {
        // ...item,
        // fundVal: Number(item.curFund.val),
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
        txnType,
        accumulatedProfit: item.accumulatedProfit,
        maxPrincipal: item.maxPrincipal,
        totalProfitRate: item.totalProfitRate,
        position: roundToFix(item.fundAmount / item.totalAmount, 4) 
      }
    })
    let data = investmentData as any as ChartSnapshot[]
    const cols = {
      date: {
        // x 轴的比例尺
        // 如果是 [0,1]: 在视图内展示所有数据
        // 如果是 [0,2]: 在2倍视图内展示所有数据
        // [0, 0.5]: 在 0.5 倍视图内展示所有数据
        range: [0, 1]
      }
    };
    if(!(data && data[0])) {
      return null
    }

    console.log('源数据', data)
    const [start, end] = [data[0].origin.date, data[data.length - 1].origin.date]
    // 过滤出当前时间范围的 数据
    const indexData = Object.values(data[0].origin.fundStrategy.indexData!).filter(item => {
      const itemDateTime = new Date(item.date).getTime()
      return itemDateTime >= new Date(start).getTime() && itemDateTime <= new Date(end).getTime()
    })
    
    let maxPos = 0
    const avgPos = roundToFix( data.reduce((result, cur) => {
      const curPos = cur.position!
      maxPos = curPos > maxPos ? curPos : maxPos
      return result + curPos
    }, 0) / data.length * 100, 2)
    
    return (
      <div >

        <FundValChart data={data} textMap={keyTextMap} commonProp={this.commonProp}  />

        <MacdLine data={indexData} textMap={keyTextMap} commonProp={this.commonProp} /> 

        <RateChart data={data} textMap={keyTextMap} commonProp={this.commonProp} />

        <TotalAmountChart data={data} textMap={keyTextMap} commonProp={this.commonProp} />

        <CommonFundLine 
          y='totalAmount'
          data={data} textMap={keyTextMap} commonProp={this.commonProp} />

        <SliderChart y='position' data={data.map(item => {
          return {
            position: item.position,
            date: item.date
          }
        })} >
        <CommonFundLine 
          y='position'
          subTitle={`平均仓位：${avgPos}%; 最大仓位：${maxPos*100}%`}
          data={data} textMap={keyTextMap} commonProp={this.commonProp} />
        </SliderChart>

        
      </div>
    );
  }
}
