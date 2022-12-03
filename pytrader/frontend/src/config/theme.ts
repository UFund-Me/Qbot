import { ITheme } from '/@/type/config/theme'
import { useLayoutStore } from '/@/store/modules/layout'

const theme:() => ITheme[] = () => {
    const { color } = useLayoutStore().getSetting
    return [
        {
            tagsActiveColor: '#fff',
            tagsActiveBg: color.primary,
            mainBg: '#f0f2f5',
            sidebarColor: '#fff',
            sidebarBg: '#001529',
            sidebarChildrenBg: '#000c17',
            sidebarActiveColor: '#fff',
            sidebarActiveBg: color.primary,
            sidebarActiveBorderRightBG: '#1890ff'
        },
        {
            tagsActiveColor: '#fff',
            tagsActiveBg: color.primary,
            navbarColor: '#fff',
            navbarBg: '#393D49',
            mainBg: '#f0f2f5',
            sidebarColor: '#fff',
            sidebarBg: '#001529',
            sidebarChildrenBg: '#000c17',
            sidebarActiveColor: '#fff',
            sidebarActiveBg: color.primary,
            sidebarActiveBorderRightBG: '#1890ff'
        },
        {
            tagsActiveColor: '#fff',
            tagsActiveBg: color.primary,
            mainBg: '#f0f2f5',
            sidebarColor: '#333',
            sidebarBg: '#fff',
            sidebarChildrenBg: '#fff',
            sidebarActiveColor: color.primary,
            sidebarActiveBg: '#e6f7ff',
            sidebarActiveBorderRightBG: color.primary
        },
        {
            logoColor: 'rgba(255,255,255,.7)',
            logoBg: '#50314F',
            tagsColor: '#333',
            tagsBg: '#fff',
            tagsActiveColor: '#fff',
            tagsActiveBg: '#7A4D7B',
            mainBg: '#f0f2f5',
            sidebarColor: 'rgba(255,255,255,.7)',
            sidebarBg: '#50314F',
            sidebarChildrenBg: '#382237',
            sidebarActiveColor: '#fff',
            sidebarActiveBg: '#7A4D7B',
            sidebarActiveBorderRightBG: '#7A4D7B'
        },
        {
            logoColor: 'rgba(255,255,255,.7)',
            logoBg: '#50314F',
            navbarColor: 'rgba(255,255,255,.7)',
            navbarBg: '#50314F',
            tagsColor: '#333',
            tagsBg: '#fff',
            tagsActiveColor: '#fff',
            tagsActiveBg: '#7A4D7B',
            mainBg: '#f0f2f5',
            sidebarColor: 'rgba(255,255,255,.7)',
            sidebarBg: '#50314F',
            sidebarChildrenBg: '#382237',
            sidebarActiveColor: '#fff',
            sidebarActiveBg: '#7A4D7B',
            sidebarActiveBorderRightBG: '#7A4D7B'
        }
    ]
}

export default theme