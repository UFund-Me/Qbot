import React, { Component } from 'react';
import Form from 'antd/es/form';
import DatePicker from 'antd/es/date-picker';
import Button from 'antd/es/button';
import Card from 'antd/es/card';
import Select from 'antd/es/select';
import InputNumber from 'antd/es/input-number';
import Cascader from 'antd/es/cascader';
import Divider from 'antd/es/divider';
import Row from 'antd/es/row';
import Col from 'antd/es/col';

import { WrappedFormUtils, FormComponentProps, GetFieldDecoratorOptions } from 'antd/lib/form/Form';
import moment from 'moment';
import { dateFormat } from '@/utils/common';
import { FundInfo, getFundInfo, IndexData } from '@/utils/fund-stragegy/fetch-fund-data';
import styles from '../index.css';
import { StopProfitForm } from './stop-profit-form';
import { BuyStragegyForm } from './buy-stragegy-form'
import { SavedSearchCondition } from './saved-search'
import throttle from 'lodash/throttle'

const { MonthPicker, RangePicker } = DatePicker;
const { Option } = Select

export interface FundFormObj {
  /**
   * 基金 id
   */
  fundId: string
  /**
   * 时间范围
   */
  dateRange: [any, any]

  /**
   * 定投周期 + 定投时间
   */
  period: ['weekly' | 'monthly', number]

  /**
   * 初始资产
   */
  totalAmount: number
  /**
   * 工资
   */
  salary: number
  /**
   * 定投资金
   */
  fixedAmount: number
  /**
   * 已买入基金
   */
  purchasedFundAmount: number


  // 止盈策略参数
  /**
   * 上证指数
   */
  shCompositeIndex: number

  /**
   * 持有仓位
   */
  fundPosition: number

  /**
   * 是否最高值止盈
   */
  sellAtTop: boolean


  /**
   * 卖出多少
   */
  sellNum: number

  /**
   * 卖出单位
   */
  sellUnit: 'amount' | 'fundPercent'

  /**
   * 持有收益率大于 xx 时止盈
   */
  profitRate: number

  /**
   * 参考指数
   */
  referIndex: string

  /**
   * 补仓macd（参考指数） 百分位临界点
   */
  buyMacdPoint: number 

  /**
   * 卖出 macd （参考指数）百分位临界点
   */
  sellMacdPoint: number 


  /**
   * 补仓买入时的 百分比
   */
  buyAmountPercent: number 
}

export interface FundSearchProp extends FormComponentProps<FundFormObj> {
  onSearch: (form: FundFormObj) => any
}


export class InnerSearchForm extends Component<FundSearchProp, {
  searchFundData: FundInfo[]
}> {

  state = {
    searchFundData: [] as FundInfo[]
  }
  private weekOpt = ['一', `二`, `三`, `四`, `五`].map((item, index) => {
    return {
      value: index + 1 as any as string,
      label: `周` + item
    }
  })

  private monthOpt = Array(28).fill('').map((item, index) => {
    return {
      value: index + 1 as any as string,
      label: `${index + 1}号`
    }
  })


  get periodOpts() {
    return [{
      value: 'weekly',
      label: '每周',
      children: this.weekOpt
    }, {
      value: 'monthly',
      label: '每月',
      children: this.monthOpt
    }]
  }

  /**
   * 基金数据搜索
   */
  handleSearch = throttle(async (value) => {
    if (value) {
      const result = await getFundInfo(value)
      this.setState({ searchFundData: result });
    } else {
      this.setState({ searchFundData: [] });
    }
  }, 1000)

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.onSearch(values)
      }
    });
  }

  reset = () => {
    this.props.form.resetFields()
  }

  private disabledDate = (date) => {
    const selectDate = new Date(date).getTime()
    const now = Date.now()
    return selectDate > now
  }

  /**
   * 当前搜索条件保存成功
   */
  // private savedSearchForm = (values: FundFormObj) => {

  // }

  /**
   * 更新当前搜索条件
   */
  private updateSearchForm = (name: string, values: FundFormObj) => {
    this.handleSearch(values.fundId)

    this.props.form.setFieldsValue({
      ...values,
      dateRange: values.dateRange.map(t => moment(t))
    })
    this.props.onSearch(values)

  }

  render() {

    const { getFieldDecorator } = this.props.form;
    const { searchFundData } = this.state
    let [curYear, curMonth, curDate] = dateFormat(new Date()).split('-').map(Number)
    curMonth = Number(curMonth) - 1

    const formItemLayout = {
      style: {
        width: 500
      },
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
      },
    };
    const rangeConfig: GetFieldDecoratorOptions = {
      rules: [{ type: 'array', required: true, message: '请选择时间范围' }],
      initialValue: [moment([Number(curYear) - 1, curMonth, curDate]), moment([curYear, curMonth, curDate])]
    };

    const colProp = {
      span: 24,
      xl: 12,
      xxl: 8
    }
    const formVal: FundFormObj = this.props.form.getFieldsValue() as any
    console.log('formVa', formVal)
    return <Card title="基金选项"
      extra={<SavedSearchCondition form={this.props.form} onSelected={this.updateSearchForm} />}
      style={{
        textAlign: 'initial',
        margin: '20px 0'
      }} >

      <Form  onSubmit={this.handleSubmit} >
        <Form.Item {...formItemLayout} label="基金编号">
          {getFieldDecorator<FundFormObj>('fundId', {
            rules: [{ required: true, message: '请输入基金编号' }],
            // initialValue: '260108'
          })(
            // <Input />
            <Select
              showSearch
              placeholder="输入基金名称或基金编号"
              defaultActiveFirstOption={false}
              showArrow={false}
              filterOption={false}
              onSearch={this.handleSearch}
              // onChange={this.handleChange}
              notFoundContent={null}
            >
              {searchFundData.map(d => <Option key={d.code}>{d.name}[{d.code}]</Option>)}
            </Select>
          )}
        </Form.Item>

        <Form.Item {...formItemLayout} label="时间范围">
          {getFieldDecorator<FundFormObj>('dateRange', rangeConfig)(
            <RangePicker
              placeholder={['开始时间', '结束时间']}
              ranges={{
                '最近一年': [moment([Number(curYear) - 1, curMonth, curDate]), moment([curYear, curMonth, curDate])],
                '最近两年': [moment([Number(curYear) - 2, curMonth, curDate]), moment([curYear, curMonth, curDate])],
                '最近三年': [moment([Number(curYear) - 3, curMonth, curDate]), moment([curYear, curMonth, curDate])],
                '最近五年': [moment([Number(curYear) - 5, curMonth, curDate]), moment([curYear, curMonth, curDate])],
              }}
              disabledDate={this.disabledDate} />)}
        </Form.Item>

        {/* 投资策略 */}
        <Row >
          <Col {...colProp} >
            <Divider orientation="left">投资策略 <span className={styles.hint}>默认[分红方式：红利复投][买入费率:0.15%][卖出费率0.5%]</span></Divider>
            <Form.Item {...formItemLayout} label="初始本金">
              {getFieldDecorator<FundFormObj>('totalAmount', {
                initialValue: 10000,
                rules: [{ required: true, message: '请输入本金' }]
              })(
                <InputNumber style={{ width: '100%' }} min={0} />
              )}
            </Form.Item>

            <Form.Item {...formItemLayout} label="月工资[每月增量资金]">
              {getFieldDecorator<FundFormObj>('salary', {
                initialValue: 10000,
                rules: [{ required: true, message: '请输入月工资' }]
              })(
                <InputNumber style={{ width: '100%' }} min={0} />
              )}
            </Form.Item>

            <Form.Item {...formItemLayout} label="初始持有基金金额">
              {getFieldDecorator<FundFormObj>('purchasedFundAmount', {
                initialValue: 0,
                rules: [{ required: true, message: '输入持有基金金额, 从0开始定投则填0' }]
              })(
                <InputNumber style={{ width: '100%' }} min={0} placeholder="投资开始时持有的基金金额" />
              )}
            </Form.Item>

            <Form.Item {...formItemLayout} label="定投金额">
              {getFieldDecorator<FundFormObj>('fixedAmount', {
                rules: [{ required: true, message: '输入定投金额' }],
                initialValue: 1000,
              })(
                <InputNumber style={{ width: '100%' }} min={0} />
              )}
            </Form.Item>

            <Form.Item {...formItemLayout} label="定投周期">
              {getFieldDecorator<FundFormObj>('period', {
                initialValue: ['monthly', 1],
                rules: [{ required: true, }],
              })(
                <Cascader options={this.periodOpts} placeholder="选择定投周期" />,
              )}

            </Form.Item>



            <Form.Item  wrapperCol={{
              sm: {
                span: 16,
                offset: 8
              }
            }}>
              <Button type="primary" htmlType="submit">
                查询
          </Button>

              <Button style={{
                marginLeft: 20
              }} onClick={this.reset} >
                重置
          </Button>
            </Form.Item>
          </Col>

          <Col {...colProp}>
          <StopProfitForm form={this.props.form} />
          </Col>
          <Col {...colProp}>
            <BuyStragegyForm form={this.props.form} />
          </Col>
        </Row>
      </Form>
      
      {
        formVal.dateRange ? 
        <div>
          <p> 定投描述：从 {formVal.dateRange[0].format('YYYY-MM-DD')} ~ {formVal.dateRange[1].format('YYYY-MM-DD')} 时间内
          投资基金[{formVal.fundId}]，初始持有基金 {formVal.purchasedFundAmount} 元，持有可用投资资金 {formVal.totalAmount} 元，每月增加投资资金 {formVal.salary}元【工资收入】；每 {formVal.period[0] === 'weekly' ? '周' : '月'} {formVal.period[1]} {formVal.period[0] === 'weekly' ? '' : '号'} 定投 {formVal.fixedAmount} 元。</p>
      <p>止盈描述：当上证指数大于 {formVal.shCompositeIndex} 点，且持有仓位大于 {formVal.fundPosition}%，且当前持有收益率大于 {formVal.profitRate}%，{formVal.sellAtTop ? '且累计盈利新高，' : ''}{formVal.sellMacdPoint !== null && formVal.sellMacdPoint >= 0 ? `且参考指数${formVal.referIndex}的MACD红柱接近 ${formVal.sellMacdPoint}% 临界位置，` : ''}则卖出 {formVal.sellNum} {formVal.sellUnit === 'amount' ? '元': '% 的持有份额'} </p>
      <p>补仓描述：{formVal.buyMacdPoint !== null && formVal.buyMacdPoint >= 0 ? `参考指数${formVal.referIndex}的MACD绿柱接近 ${formVal.buyMacdPoint}% 临界位置，买入剩余流动资金的 ${formVal.buyAmountPercent}%` : ''}</p>
        </div> : null
      }
      
    </Card>
  }
}

export const SearchForm = Form.create<FundSearchProp>({ name: 'fund-search' })(InnerSearchForm);
