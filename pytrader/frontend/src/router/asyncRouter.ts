import { IMenubarList } from '/@/type/store/layout'
import { listToTree } from '/@/utils/tools'
import { useLayoutStore } from '/@/store/modules/layout'

// 动态路由名称映射表
const modules = import.meta.glob('../views/**/**.vue')
const components:IObject<() => Promise<typeof import('*.vue')>> = {
    Layout: (() => import('/@/layout/index.vue')) as unknown as () => Promise<typeof import('*.vue')>
}
Object.keys(modules).forEach(key => {
    const nameMatch = key.match(/^\.\.\/views\/(.+)\.vue/)
    if(!nameMatch) return
    // 排除_Components文件夹下的文件
    if(nameMatch[1].includes('_Components')) return
    // 如果页面以Index命名，则使用父文件夹作为name
    const indexMatch = nameMatch[1].match(/(.*)\/Index$/i)
    let name = indexMatch ? indexMatch[1] : nameMatch[1];
    [name] = name.split('/').splice(-1)
    components[name] = modules[key] as () => Promise<typeof import('*.vue')>
})

const asyncRouter:IMenubarList[] = [
    {
        path: '/:pathMatch(.*)*', 
        name: 'NotFound', 
        component: components['404'],
        meta: {
            title: 'NotFound',
            icon: '',
            hidden: true
        }, 
        redirect: {
            name: '404'
        }
    }
]

const generatorDynamicRouter = (data:IMenubarList[]):void => {
    const { setRoutes } = useLayoutStore()
    const routerList:IMenubarList[] = listToTree(data, 0)
    asyncRouter.forEach(v => routerList.push(v))
    const f = (data:IMenubarList[], pData:IMenubarList|null) => {
        for(let i = 0,len = data.length;i < len;i++) {
            const v:IMenubarList = data[i]
            if(typeof v.component === 'string') v.component = components[v.component]
            if(!v.meta.permission || pData && v.meta.permission.length === 0) {
                v.meta.permission = pData && pData.meta && pData.meta.permission ? pData.meta.permission : []
            }
            if(v.children && v.children.length > 0) {
                f(v.children, v)
            }
        }
    }
    f(routerList, null)
    setRoutes(routerList)
}

export {
    components,
    generatorDynamicRouter
}
