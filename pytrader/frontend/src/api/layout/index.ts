import request from '/@/utils/request'
import { AxiosResponse } from 'axios'
import { IMenubarList } from '/@/type/store/layout'

const api = {
    login: '/api/login',
    getUser: '/api/me',
    getRouterList: '/api/route',
    getStocks: '/api/stocks',
    publickey: '/api/User/Publickey'
}

export interface loginParam {
    username: string,
    password: string
}

export function login(param: loginParam):Promise<AxiosResponse<ILoginResult>> {
    return request({
        url: api.login,
        method: 'post',
        data: param
    })
}

export function publickey():Promise<AxiosResponse<IResponse<string>>> {
    return request({
        url: api.publickey,
        method: 'get'
    })
}

interface IGetuserRes {
    username: string
    roles: Array<string>
}

interface ILoginResult {
    access_token: string
    token_type: string
}

export interface IStocks {
    code: string
    name: string
    watch_price: number
    watch_time: string
    close: number
    now: number
    [key: string]: any
}

export function getUser(): Promise<AxiosResponse<IGetuserRes>> {
    return request({
        url: api.getUser,
        method: 'get'
    })
}

export function getRouterList(): Promise<AxiosResponse<Array<IMenubarList>>> {
    return request({
        url: api.getRouterList,
        method: 'get'
    })
}

export function getStocks(): Promise<AxiosResponse<Array<IStocks>>> {
    return request({
        url: api.getStocks,
        method: 'get'
    })
}


export function addStock(code:string): Promise<AxiosResponse<any>> {
    return request({
        url: `/api/watch_stocks/${code}`,
        method: 'post'
    })
}

export function removeWatchStock(code:string): Promise<AxiosResponse<any>> {
    return request({
        url: `/api/watch_stocks/${code}`,
        method: 'delete'
    })
}

export function get_balance(): Promise<AxiosResponse<any>> {
    return request({
        url: '/api/balance',
        method: 'get'
    })
}

export function get_position(): Promise<AxiosResponse<any>> {
    return request({
        url: '/api/position',
        method: 'get'
    })
}

export function get_entrust(): Promise<AxiosResponse<any>> {
    return request({
        url: '/api/entrust',
        method: 'get'
    })
}

export function get_current_deal(): Promise<AxiosResponse<any>> {
    return request({
        url: '/api/deal',
        method: 'get'
    })
}

export function buy(): Promise<AxiosResponse<any>> {
    return request({
        url: '/api/balance',
        method: 'get'
    })
}


export function sell(): Promise<AxiosResponse<any>> {
    return request({
        url: '/api/balance',
        method: 'get'
    })
}