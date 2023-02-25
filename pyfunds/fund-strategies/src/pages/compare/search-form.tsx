

import React, {Component} from 'react'
import Form from 'antd/es/form';
import Card from 'antd/es/card'
import Checkbox from 'antd/es/checkbox'
import Row from 'antd/es/row'
import Col from 'antd/es/col'
import DatePicker from 'antd/es/date-picker'
import Button from 'antd/es/button'

import { FormComponentProps } from 'antd/lib/form';
import { allSavedCondition } from '../components/saved-search';
import moment from 'moment'
import { GetFieldDecoratorOptions } from 'antd/lib/form/Form';
import { dateFormat, disabledFuture } from '@/utils/common';

import {keyTextMap} from '../components/fund-line'
const { RangePicker } = DatePicker;
let [curYear, curMonth, curDate] = dateFormat(new Date()).split('-').map(Number)
curMonth = Number(curMonth) - 1

/**
 * 没有必要进行对比的数据
 */
const excludeList: (keyof typeof keyTextMap)[] = ['fundVal', 'dateBuyAmount', 'dateSellAmount', 'buy','fixedBuy','sell']

const checkList: (keyof typeof keyTextMap)[] = ['totalAmount','leftAmount', 'profitRate', 'profit', 'fundAmount', 'fundGrowthRate', 'maxPrincipal','accumulatedProfit', 'totalProfitRate', 'position'] 

interface CompareFormProp extends FormComponentProps{
  onSearch: (val: CompareFormObj)=>void
}
export interface CompareFormObj {
  /**
   * 选择了的策略
   */
  stragegyChecked: string[]

  /**
   * 要对比的数据
   */
  chartChecked: string[]
  dateRange: [any, any]
}

const formItemLayout = {
  // style: {
  //   width: 500
  // },
  labelCol: {
    xs: { span: 24 },
    sm: { span: 4 },
  },
  wrapperCol: {
    xs: { span: 24 },
    sm: { span: 20 },
  },
};


export class CompareForm extends  Component<CompareFormProp> {


  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('compare表单', values)
        this.props.onSearch(values)
      }
    });
  }

  render() {
    const { getFieldDecorator } = this.props.form

    
    const rangeConfig: GetFieldDecoratorOptions = {
      rules: [{ type: 'array', required: true, message: '请选择时间范围' }],
      initialValue: [moment([Number(curYear) - 1, curMonth, curDate]), moment([curYear, curMonth, curDate])]
    };
    return <Card title="基金策略比较"  style={{
      textAlign: 'initial',
      margin: '20px 0'
    }} >
      <Form  onSubmit={this.handleSubmit} >
      <Form.Item {...formItemLayout} label="已有基金策略" >
        {
          getFieldDecorator<CompareFormObj>('stragegyChecked', {
            rules: [{ required: true, message: '请至少选择一个基金策略' }],
          })(<Checkbox.Group style={{ width: '100%' }}>
            {Object.keys(allSavedCondition).map((tagName,index) => <Checkbox key={index} value={tagName}>{tagName}</Checkbox>)}
        </Checkbox.Group>)
        }
        </Form.Item>

        <Form.Item {...formItemLayout} label="对比的数据" >
        {
          getFieldDecorator<CompareFormObj>('chartChecked', {
            initialValue: ['totalAmount', 'accumulatedProfit', 'totalProfitRate', 'position'],
            rules: [{ required: true, message: '请至少选择一个数据' }],
          })(<Checkbox.Group style={{ width: '100%' }}>
            {checkList.map((key,index) => <Checkbox key={index} value={key}>{keyTextMap[key]}</Checkbox>)}
        </Checkbox.Group>)
        }
        </Form.Item>

        
        <Form.Item {...formItemLayout} label="时间范围">
          {getFieldDecorator<CompareFormObj>('dateRange', rangeConfig)(
            <RangePicker
              placeholder={['开始时间', '结束时间']}
              ranges={{
                '最近一年': [moment([Number(curYear) - 1, curMonth, curDate]), moment([curYear, curMonth, curDate])],
                '最近两年': [moment([Number(curYear) - 2, curMonth, curDate]), moment([curYear, curMonth, curDate])],
                '最近三年': [moment([Number(curYear) - 3, curMonth, curDate]), moment([curYear, curMonth, curDate])],
                '最近五年': [moment([Number(curYear) - 5, curMonth, curDate]), moment([curYear, curMonth, curDate])],
              }}
              disabledDate={disabledFuture} />)}
        </Form.Item>

        <Form.Item wrapperCol={{   offset: 4 }}>
          <Button type="primary" htmlType="submit">
            比较策略
          </Button>
        </Form.Item>

        </Form>
      </Card>
  }
}

export const CompareSearchForm = Form.create<CompareFormProp>({ name: 'compare-search' })(CompareForm);