<template>
    <el-scrollbar>
        <router-view v-slot='{ Component }'>
            <transition name='fade-transform' mode='out-in'>  
                <keep-alive :include='setting.showTags ? data.cachedViews : []'>
                    <component :is='Component' :key='key' class='page m-3 relative' />
                </keep-alive>
            </transition>
        </router-view>
        <el-backtop target='.layout-main-content>.el-scrollbar>.el-scrollbar__wrap' :bottom='15' :right='15'>
            <div><i class='el-icon-caret-top' /></div>
        </el-backtop>
    </el-scrollbar>
</template>

<script lang='ts'>
import { computed, defineComponent, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useLayoutStore } from '/@/store/modules/layout'

export default defineComponent ({
    name: 'LayoutContent',
    setup() {
        const route = useRoute()
        const { getSetting, getTags } = useLayoutStore()

        const key = computed(() => route.path)

        let data = reactive({
            cachedViews: [...getTags.cachedViews]
        })
        // keep-alive的include重新赋值，解决bug https://github.com/vuejs/vue-next/issues/2550
        watch(
            () => getTags.cachedViews.length,
            () => data.cachedViews = [...getTags.cachedViews]
        )
        return {
            key,
            data,
            setting: getSetting
        }
    }
})
</script>

<style lang='postcss' scoped>

::v-deep(.el-card) {
    overflow: visible;
}

/* ::v-deep(.el-scrollbar__view) {
    height: 100%;
} */

.fade-transform-leave-active,
.fade-transform-enter-active {
    transition: all 0.5s;
}

.fade-transform-enter-from {
    opacity: 0;
    transform: translateX(-30px);
}

.fade-transform-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
</style>