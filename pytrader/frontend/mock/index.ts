import { MockMethod } from 'vite-plugin-mock'
import { mock, Random } from 'mockjs'
import { login, setToken, checkToken, getUser, getRoute } from '/mock/response'

export interface IReq { 
    body: any; 
    query: any, 
    headers: any; 
}

Random.extend({
    tag: function() {
        const tag = ['家', '公司', '学校', '超市']
        return this.pick(tag)
    }
})
interface ITableList {
    list: Array<{
        date: string
        name: string
        address: string
        tag: '家' | '公司' | '学校' | '超市'
        amt: number
    }>
}
const tableList: ITableList = mock({
    // 属性 list 的值是一个数组，其中含有 1 到 10 个元素
    'list|100': [{
        // 属性 id 是一个自增数，起始值为 1，每次增 1
        'id|+1': 1,
        date: () => Random.date('yyyy-MM-dd'),
        name: () => Random.name(),
        address: () => Random.cparagraph(1),
        tag: () => Random.tag(),
        amt: () => Number(Random.float(-100000,100000).toFixed(2))
    }]
})

const responseData = (code: number, msg: string, data: any) => {
    return {
        Code: code,
        Msg: msg,
        Data: data
    }
}

export default [
    {
        url: '/api/User/login',
        method: 'post',
        timeout: 300,
        response: (req: IReq) => {
            const { username, password } = req.body
            if(login(username, password)) return responseData(200, '登陆成功', setToken(username))
            return responseData(401, '用户名或密码错误', '')
        }
    },
    {
        url: '/api/User/getUser',
        method: 'get',
        timeout: 300,
        response: (req: IReq) => {
            const userName = checkToken(req)
            if(!userName) return responseData(401, '身份认证失败', '')
            return responseData(200, '', getUser(userName))
        }
    },
    {
        url: '/api/User/getRoute',
        method: 'get',
        timeout: 300,
        response: (req: IReq) => {
            const userName = checkToken(req)
            if(!userName) return responseData(401, '身份认证失败', '')
            return responseData(200, '', getRoute(userName))
        }
    },
    {
        url: '/api/getTableList',
        method: 'get',
        timeout: 600,
        response: (req: IReq) => {
            const userName = checkToken(req)
            if(!userName) return responseData(401, '身份认证失败', '')
            const { page, size, tag } = req.query
            const data = tag === '所有' ? tableList.list : tableList.list.filter(v => v.tag === tag)
            const d = {
                data: data.filter((v,i) => i >= (page - 1) * size && i < page * size),
                total: data.length
            }
            return responseData(200, '', d)
        }
    }
] as MockMethod[]
