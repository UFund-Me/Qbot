<template>
    <div class='hidden-xs-only px-2'>
        <svg-icon v-if='!isFullscreen' class-name='cursor-pointer' icon-class='svg-fullscreen' @click='changeScreenfull' />
        <svg-icon v-else class-name='cursor-pointer' icon-class='svg-exit-fullscreen' @click='changeScreenfull' />
        
        <!-- 切换失效 -->
        <!-- <svg-icon class-name='cursor-pointer' :icon-class='isFullscreen ? "svg-exit-fullscreen" : "svg-fullscreen"' @click='changeScreenfull' /> -->
    </div>
</template>
<script lang='ts'>
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import screenfull from 'screenfull'
import { ElNotification } from 'element-plus'

export default defineComponent({
    name: 'Screenfull',
    setup() {
        const isFullscreen = ref(false)
        const changeScreenfull = () => {
            if (!screenfull.isEnabled) {
                ElNotification({
                    message: '浏览器不支持全屏',
                    type: 'warning'
                })
            }else{
                screenfull.toggle()
            }
        }
        const change = () => {
            if(screenfull.isEnabled) isFullscreen.value = screenfull.isFullscreen
        }
        onMounted(() => screenfull.isEnabled && screenfull.on('change', change))
        onUnmounted(() => screenfull.isEnabled && screenfull.off('change', change))
        return {
            isFullscreen,
            changeScreenfull
        }
    }
})
</script>