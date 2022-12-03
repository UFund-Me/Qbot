import request from '/@/utils/request'
import { AxiosResponse } from 'axios'
const api = {
    getTableList: '/api/getTableList'
}
export type ITag = '所有' | '家' | '公司' | '学校' | '超市'
export interface ITableList {
    page: number
    size: number
    tag: ITag
}
export function getTableList(tableList: ITableList): Promise<AxiosResponse<IResponse>> {
    return request({
        url: api.getTableList,
        method: 'get',
        params: tableList
    })
}