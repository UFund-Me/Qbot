
import router from '/@/router/index'
export type IPermissionType = 'or' | 'and'
export function checkPermission(permission:string|Array<string>, type:IPermissionType = 'or'):boolean {
    const value:Array<string> = typeof permission === 'string' ? [permission] : permission
    const currentRoute = router.currentRoute.value
    const roles:Array<string> = (currentRoute.meta.permission || []) as Array<string>
    const isShow = type === 'and' 
        ? value.every(v => roles.includes(v))
        : value.some(v => roles.includes(v))

    return isShow
}