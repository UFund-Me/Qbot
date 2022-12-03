<template>
    <div class='layout flex h-screen'>
        <div class='layout-sidebar-mask fixed w-screen h-screen bg-black bg-opacity-25 z-20' :class='{"hidden": getMenubar.status !== 2 }' @click='changeCollapsed' />
        <div
            v-if='getSetting.mode === "vertical" || getMenubar.isPhone'
            class='layout-sidebar flex flex-col h-screen transition-width duration-200 shadow'
            :class='{ 
                "w-64": getMenubar.status === 0 || getMenubar.status === 2, 
                "w-0": getMenubar.status === 3, 
                "w-16": getMenubar.status === 1, 
                "absolute z-30": getMenubar.status === 2 || getMenubar.status === 3, 
            }'
        >
            <div class='layout-sidebar-logo flex h-12 relative flex-center shadow-lg'>
                <span v-if='getMenubar.status === 0 || getMenubar.status === 2' class='pl-2'>PyTrader</span>
            </div>
            <div class='layout-sidebar-menubar flex flex-1 overflow-hidden'>
                <el-scrollbar wrap-class='scrollbar-wrapper'>
                    <layout-menubar />
                </el-scrollbar>
            </div>
        </div>
        <div class='layout-main flex flex-1 flex-col overflow-x-hidden overflow-y-auto'>
            <div class='layout-main-navbar flex justify-between items-center h-12 shadow-sm overflow-hidden relative z-10'>
                <layout-navbar />
            </div>
            <div
                v-if='getSetting.showTags'
                class='layout-main-tags h-8 leading-8 text-sm text-gray-600 relative'
            >
                <layout-tags />
            </div>
            <div class='layout-main-content flex-1 overflow-hidden'>
                <layout-content />
            </div>
        </div>
        <div class='layout-sidebar-sidesetting fixed right-0 top-64 z-10'>
            <layout-side-setting />
        </div>
    </div>
</template>

<script lang='ts'>
import { defineComponent, onMounted } from 'vue'
import LayoutContent from '/@/layout/components/content.vue'
import LayoutMenubar from '/@/layout/components/menubar.vue'
import LayoutNavbar from '/@/layout/components/navbar.vue'
import LayoutTags from '/@/layout/components/tags.vue'
import LayoutSideSetting from '/@/layout/components/sideSetting.vue'
import { throttle } from '/@/utils/tools'
import { useLayoutStore } from '/@/store/modules/layout'
import icon from '/@/assets/img/icon.png'

export default defineComponent ({
    name: 'Layout',
    components: {
        LayoutContent,
        LayoutMenubar,
        LayoutNavbar,
        LayoutTags,
        LayoutSideSetting
    },
    setup() {
        const { changeDeviceWidth, changeCollapsed, getMenubar, getSetting } = useLayoutStore()

        onMounted(async() => {
            changeDeviceWidth()
            const throttleFn = throttle(300)
            let throttleF = async function() {
                await throttleFn()
                changeDeviceWidth()
            }
            window.addEventListener('resize', throttleF, true)
        })

        return {
            getMenubar,
            getSetting,
            changeCollapsed,
            icon
        }
    }
})
</script>

<style lang='postcss' scoped>
    ::v-deep(.layout-sidebar-sidesetting .el-drawer__header) {
        margin-bottom: 0;
    }

    ::v-deep(.el-menu--horizontal>.el-menu-item) {
        height: 48px;
    }

    ::v-deep(.el-menu--horizontal>.el-sub-menu .el-sub-menu__title) {
        height: 48px;
        line-height: 48px;
    }
</style>