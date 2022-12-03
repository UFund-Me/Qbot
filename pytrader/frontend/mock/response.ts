import { user, user_role, role_route, route } from '/mock/data/user'
import { IMenubarList } from '/@/type/store/layout'
import { IReq } from '/mock/index'

export const setToken = function(name: string):string {
    return `token_${name}_token`
}

export const checkToken = function(req:IReq):string {
    const token = req.headers['access-token']
    const match = token.match(/^token_([\w|\W]+?)_token/)
    const userName = match ? match[1] : ''
    return userName
}

export const login = function(name: string, pwd: string):boolean {
    return user.findIndex(v => v.name === name && v.pwd === pwd) !== -1
}

export const getUser = function(name: string):{name:string, role: Array<string>} {
    return {
        name,
        role: user_role.filter(v => v.userName === name).map(v => v.roleName)
    }
}

export const getRoute = function(name: string):Array<IMenubarList> {
    const { role } = getUser(name)
    const arr = role_route.filter(v => role.findIndex(val => val === v.roleName) !== -1)
    const filterRoute:Array<IMenubarList> = []
    route.forEach(v => {
        arr.forEach(val => {
            if(val.id === v.id) {
                const obj = Object.assign({},v)
                obj.meta.permission = val.permission
                filterRoute.push(obj)
            }
        })
    })
    return filterRoute
}