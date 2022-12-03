import { defineStore } from 'pinia'
import { login, loginParam, getRouterList, getUser } from '/@/api/layout/index'
import { ILayout, IMenubarStatus, ITagsList, IMenubarList, ISetting, IMenubar, IStatus, ITags, IUserInfo } from '/@/type/store/layout'
import router from '/@/router/index'
import { allowRouter } from '/@/router/index'
import { generatorDynamicRouter } from '/@/router/asyncRouter'
import { setLocal, getLocal, decode } from '/@/utils/tools'
import { RouteLocationNormalizedLoaded } from 'vue-router'

const setting = getLocal<ISetting>('setting')
const { ACCESS_TOKEN } = getLocal<IStatus>('token')

export const useLayoutStore = defineStore({
    id: 'layout',
    state: (): ILayout => ({
        menubar: {
            status: document.body.offsetWidth < 768 ? IMenubarStatus.PHN : IMenubarStatus.PCE,
            menuList: [],
            isPhone: document.body.offsetWidth < 768
        },
        // 用户信息
        userInfo: {
            name: '',
            role: []
        },
        // 标签栏
        tags: {
            tagsList: [],
            cachedViews: []
        },
        setting: {
            theme: setting.theme !== undefined ? setting.theme : 0,
            showTags: setting.showTags !== undefined ? setting.showTags : true,
            color: {
                primary: setting.color !== undefined ? setting.color.primary : '#409eff'
            },
            usePinyinSearch: setting.usePinyinSearch !== undefined ? setting.usePinyinSearch : false,
            mode: setting.mode || 'vertical'
        },
        status: {
            isLoading: false,
            ACCESS_TOKEN: ACCESS_TOKEN || ''
        }
    }),
    getters: {
        getMenubar(): IMenubar {
            return this.menubar
        },
        getUserInfo(): IUserInfo {
            return this.userInfo
        },
        getTags(): ITags {
            return this.tags
        },
        getSetting(): ISetting {
            return this.setting
        },
        getStatus(): IStatus {
            return this.status
        }
    },
    actions: {
        changeCollapsed(): void {
            this.menubar.status = this.menubar.isPhone
                ? this.menubar.status === IMenubarStatus.PHN
                    ? IMenubarStatus.PHE
                    : IMenubarStatus.PHN
                : this.menubar.status === IMenubarStatus.PCN
                    ? IMenubarStatus.PCE
                    : IMenubarStatus.PCN
        },
        changeDeviceWidth(): void {
            this.menubar.isPhone = document.body.offsetWidth < 768
            this.menubar.status = this.menubar.isPhone ? IMenubarStatus.PHN : IMenubarStatus.PCE
        },
        // 切换导航，记录打开的导航
        changeTagNavList(cRouter: RouteLocationNormalizedLoaded): void {
            if (!this.setting.showTags) return // 判断是否开启多标签页
            // if(cRouter.meta.hidden && !cRouter.meta.activeMenu) return // 隐藏的菜单如果不是子菜单则不添加到标签
            if (new RegExp('^\/redirect').test(cRouter.path)) return
            const index = this.tags.tagsList.findIndex(v => v.path === cRouter.path)
            this.tags.tagsList.forEach(v => v.isActive = false)
            // 判断页面是否打开过
            if (index !== -1) {
                this.tags.tagsList[index].isActive = true
                return
            }
            const tagsList: ITagsList = {
                name: cRouter.name as string,
                title: cRouter.meta.title as string,
                path: cRouter.path,
                isActive: true
            }
            this.tags.tagsList.push(tagsList)
        },
        removeTagNav(obj: { tagsList: ITagsList, cPath: string }): void {
            const index = this.tags.tagsList.findIndex(v => v.path === obj.tagsList.path)
            if (this.tags.tagsList[index].path === obj.cPath) {
                this.tags.tagsList.splice(index, 1)
                const i = index === this.tags.tagsList.length ? index - 1 : index
                this.tags.tagsList[i].isActive = true
                this.removeCachedViews({ name: obj.tagsList.name, index })
                router.push({ path: this.tags.tagsList[i].path })
            } else {
                this.tags.tagsList.splice(index, 1)
                this.removeCachedViews({ name: obj.tagsList.name, index })
            }
        },
        removeOtherTagNav(tagsList: ITagsList): void {
            const index = this.tags.tagsList.findIndex(v => v.path === tagsList.path)
            this.tags.tagsList.splice(index + 1)
            this.tags.tagsList.splice(0, index)
            this.tags.cachedViews.splice(index + 1)
            this.tags.cachedViews.splice(0, index)
            router.push({ path: tagsList.path })
        },
        removeAllTagNav(): void {
            this.tags.tagsList.splice(0)
            this.tags.cachedViews.splice(0)
            router.push({ path: '/redirect/' })
        },
        // 添加缓存页面
        addCachedViews(obj: { name: string, noCache: boolean }): void {
            if (!this.setting.showTags) return // 判断是否开启多标签页
            if (obj.noCache || this.tags.cachedViews.includes(obj.name)) return
            this.tags.cachedViews.push(obj.name)
        },
        // 删除缓存页面
        removeCachedViews(obj: { name: string, index: number }): void {
            // 判断标签页是否还有该页面
            if (this.tags.tagsList.map(v => v.name).includes(obj.name)) return
            this.tags.cachedViews.splice(obj.index, 1)
        },
        logout(): void {
            this.status.ACCESS_TOKEN = ''
            localStorage.removeItem('token')
            history.go(0)
        },
        setToken(token: string): void {
            this.status.ACCESS_TOKEN = token
            setLocal('token', this.status, 1000 * 60 * 60)
        },
        setRoutes(data: Array<IMenubarList>): void {
            this.menubar.menuList = data
        },
        concatAllowRoutes(): void {
            allowRouter.reverse().forEach(v => this.menubar.menuList.unshift(v))
        },
        // 修改主题
        changeTheme(num?: number): void {
            if (num === this.setting.theme) return
            if (typeof num !== 'number') num = this.setting.theme
            this.setting.theme = num
            localStorage.setItem('setting', JSON.stringify(this.setting))
        },
        // 修改主题色
        changeThemeColor(color: string): void {
            this.setting.color.primary = color
            localStorage.setItem('setting', JSON.stringify(this.setting))
        },
        changeTagsSetting(showTags: boolean): void {
            this.setting.showTags = showTags
            localStorage.setItem('setting', JSON.stringify(this.setting))

            if (showTags) {
                const index = this.tags.tagsList.findIndex(v => v.path === router.currentRoute.value.path)
                if (index !== -1) {
                    this.tags.tagsList.forEach(v => v.isActive = false)
                    this.tags.tagsList[index].isActive = true
                } else {
                    this.changeTagNavList(router.currentRoute.value)
                }
            }
        },
        changePinSearchSetting(showPinyinSearch: boolean): void {
            this.setting.usePinyinSearch = showPinyinSearch
            localStorage.setItem('setting', JSON.stringify(this.setting))
        },
        // 下次进去该页面刷新该页面(解决子页面保存之后，回到父页面页面不刷新问题)
        refreshPage(path: string): void {
            const name = this.tags.tagsList.filter(v => v.path === path)[0]?.name
            if (!name) return
            const index = this.tags.cachedViews.findIndex(v => v === name)
            this.tags.cachedViews.splice(index, 1)
        },
        changemenubarMode(mode: 'horizontal' | 'vertical'): void {
            this.setting.mode = mode
            localStorage.setItem('setting', JSON.stringify(this.setting))
        },
        async login(param: loginParam): Promise<void> {
            const res = await login(param)
            const token = res.data.access_token
            this.status.ACCESS_TOKEN = token
            setLocal('token', this.status, 1000 * 60 * 60)
            const { query } = router.currentRoute.value
            router.push(typeof query.from === 'string' ? decode(query.from) : '/')
        },
        async getUser(): Promise<void> {
            const res = await getUser()
            const userInfo = res.data
            this.userInfo.name = userInfo.username
            this.userInfo.role = userInfo.roles
        },
        async GenerateRoutes(): Promise<void> {
            const res = await getRouterList()
            generatorDynamicRouter(res.data)
        }
    }
})