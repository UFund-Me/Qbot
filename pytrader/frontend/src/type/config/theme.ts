
export interface ITheme {
    // logo不传则使用侧边栏sidebar样式
    logoColor?: string
    logoBg?: string
    // 顶部导航栏和标签栏不传则背景色使用白色，字体颜色默认
    navbarColor?: string
    navbarBg?: string
    tagsColor?: string
    tagsBg?: string
    tagsActiveColor?: string
    tagsActiveBg?: string
    mainBg: string
    sidebarColor: string
    sidebarBg: string
    sidebarChildrenBg: string
    sidebarActiveColor: string
    sidebarActiveBg: string
    sidebarActiveBorderRightBG?: string
}