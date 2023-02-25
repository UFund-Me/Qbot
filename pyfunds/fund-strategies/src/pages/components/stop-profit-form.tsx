import React, { Component, Fragment } from 'react';
import { FundFormObj } from './search-form';
import Form, { FormComponentProps } from 'antd/lib/form';
import Divider from 'antd/es/divider'
import InputNumber from 'antd/es/input-number'
import Switch from 'antd/es/switch'
import Select from 'antd/es/select'
import Row from 'antd/es/row'
import Col from 'antd/es/col'
import { searchIndex, SearchIndexResp } from '@/utils/fund-stragegy/fetch-fund-data';
import throttle from 'lodash/throttle'


const { Option } = Select
interface StopProfitFormProp {
  // form: 
}

export class StopProfitForm extends Component<FormComponentProps<FundFormObj>>{
  state = {
    searchIndexData:  [] as SearchIndexResp[] 
  }
  
  
  handleSearchIndex = throttle(async (value)=>{
    
    if (value) {
      const result = await searchIndex(value)
      this.setState({ searchIndexData: result });
    } else {
      this.setState({ searchIndexData: [] });
    }
  }, 1000)

  render() {
    const { searchIndexData } = this.state
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
    const { getFieldDecorator, getFieldsValue } = this.props.form;
    const fieldsVal = getFieldsValue()
    // 最大止盈卖出
    const maxSell = fieldsVal.sellUnit === 'fundPercent' ? 100 : undefined

    return <section>
      {/* 投资策略 */}
      <Divider orientation="left">止盈策略 </Divider>

      <Form.Item {...formItemLayout} label='上证指数大于'>
        {getFieldDecorator<FundFormObj>('shCompositeIndex', {
          initialValue: 3000,
        })(
          <InputNumber style={{ width: '100%' }} min={0} placeholder="大于上证指数的点，则开始进行止盈" />
        )}
      </Form.Item>

      <Form.Item {...formItemLayout} label='持有仓位大于'>
        {getFieldDecorator<FundFormObj>('fundPosition', {
          initialValue: 70,
        })(
          <InputNumber style={{ width: '100%' }}
            formatter={value => `${value}%`}
            parser={value => value ? value.replace('%', '') : ''}
            min={0} max={100} placeholder="持仓大于多少时开始止盈" />
        )}
      </Form.Item>

      <Form.Item {...formItemLayout} label='持有收益率大于'>
        {getFieldDecorator<FundFormObj>('profitRate', {
          initialValue: 5,
        })(
          <InputNumber style={{ width: '100%' }}
            formatter={value => `${value}%`}
            parser={value => value ? value.replace('%', '') : ''}
            min={0} placeholder="开始止盈的持有收益率最小值" />
        )}
      </Form.Item>

      <Form.Item {...formItemLayout} label='是否收益新高'>
        {getFieldDecorator<FundFormObj>('sellAtTop', {
          initialValue: true,
          valuePropName: 'checked'
        })(
          <Switch checkedChildren="是" unCheckedChildren="否" />
        )}
      </Form.Item>

      <Form.Item {...formItemLayout} label='卖出金额'>
        <Row>
          <Col span={12}>
            {getFieldDecorator<FundFormObj>('sellNum', {
              initialValue: 10,
            })(
              <InputNumber style={{width: '100%'}} min={0} max={maxSell} placeholder="止盈时卖出多少" />
            )}
          </Col>
          <Col span={12}>
            <Form.Item style={{marginBottom: 'unset'}}>
            {getFieldDecorator<FundFormObj>('sellUnit', {
              initialValue: 'fundPercent',
            })(
              <Select >
                <Option value="amount">元</Option>
                <Option value="fundPercent">% 持有份额</Option>
              </Select>
            )}
            </Form.Item>
          </Col>
        </Row>
      </Form.Item>

      <Form.Item {...formItemLayout} label="指数编号/名称">
          {getFieldDecorator<FundFormObj>('referIndex', {
            // rules: [{ required: true, message: '请输入指数名称' }],
            initialValue: '1.000001'
          })(
            // <Input />
            <Select
              showSearch
              placeholder="输入指数名称或编号"
              defaultActiveFirstOption={false}
              showArrow={false}
              filterOption={false}
              onSearch={this.handleSearchIndex}
              // onChange={this.handleChange}
              notFoundContent={null}
            >
              {searchIndexData.map((d, index) => <Option key={d.id}>{d.name}[{d.code}]</Option>)}
            </Select>
          )}
        </Form.Item>

        <Form.Item {...formItemLayout} label="卖出 MACD 临界点">
        {getFieldDecorator<FundFormObj>('sellMacdPoint', {
          // initialValue: 100
        })(
          <InputNumber style={{width: '100%'}} formatter={value => `${value}%`}
          parser={value => (value || '').replace('%', '')}  min={0} max={100} placeholder="macd 止盈点" />
        )
        }
        </Form.Item>
    </section>
  }
}