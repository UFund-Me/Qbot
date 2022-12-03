<template>
    <div class='shadow border-b border-gray-100 px-3 overflow-hidden relative z-10'>
        <el-scrollbar ref='scrollbar' wrap-class='scrollbar-wrapper'>
            <div class='layout-tags-container whitespace-nowrap'>
                <span
                    v-for='v in tagsList'
                    :key='v.path'
                    :ref='getTagsDom'
                    class='border border-gray-200 px-2 py-1 mx-1 cursor-pointer'
                    :class='{"layout-tags-active": v.isActive}'
                    @contextmenu.prevent='contextRightMenu(v,$event)'
                >
                    <i v-if='v.isActive' class='rounded-full inline-block w-2 h-2 bg-white -ml-1 mr-1' />
                    <router-link :to='v.path'>{{ v.title }}</router-link>
                    <i v-if='tagsList.length>1' class='el-icon-close text-xs hover:bg-gray-300 hover:text-white rounded-full leading-3 p-0.5 ml-1 -mr-1' @click='removeTag(v)' />
                </span>
            </div>
        </el-scrollbar>
    </div>
    <ul ref='rightMenuEl' class='border border-gray-200 absolute w-24 leading-none bg-white shadow-md rounded-lg py-0.5 z-10' :style='menuPos'>
        <li class='px-4 py-2 cursor-pointer hover:bg-gray-200' @click='refresh'>刷新</li>
        <li class='px-4 py-2 cursor-pointer hover:bg-gray-200' @click='closeOther'>关闭其它</li>
        <li class='px-4 py-2 cursor-pointer hover:bg-gray-200' @click='removeAllTagNav'>关闭所有</li>
    </ul>
</template>

<script lang="ts">
import { defineComponent, nextTick, ref, watch, onBeforeUpdate, onMounted, reactive, Ref, ComponentInternalInstance } from 'vue'
import { useLayoutStore } from '/@/store/modules/layout'
import { useRoute, useRouter } from 'vue-router'
import { ITagsList } from '/@/type/store/layout'

// 右键菜单
const rightMenu = () => {
    const { removeOtherTagNav } = useLayoutStore()
    const route = useRoute()
    const router = useRouter()
    const menuPos = reactive({
        left: '0px',
        top: '0px',
        display: 'none'
    })
    const rightMenuEl:Ref<HTMLElement | null> = ref(null)
    // 当前右键的那个标签
    let currentRightTags:ITagsList
    const contextRightMenu = (v:ITagsList, event:MouseEvent) => {
        currentRightTags = v
        menuPos.display = 'block'
        nextTick(() => {
            if(!rightMenuEl.value) return
            const parentNode = rightMenuEl.value?.parentNode as HTMLElement
            let left = event.clientX - parentNode.offsetLeft - 5
            let top = event.clientY - parentNode.offsetTop + 10
            if(event.clientX + rightMenuEl.value.offsetWidth > document.body.offsetWidth) {
                left = left - rightMenuEl.value.offsetWidth + 15
            }
            menuPos.left = `${left}px`
            menuPos.top = `${top}px`
        })
    }
    const refresh = () => {
        if(currentRightTags.path === route.path) {
            router.replace(`/redirect${currentRightTags.path}`)
        }else{
            router.push(`/redirect${currentRightTags.path}`)
        }
    }
    const closeOther = () => removeOtherTagNav(currentRightTags)
    document.body.addEventListener('click', () => menuPos.display = 'none')
    return { menuPos, contextRightMenu, refresh, rightMenuEl, closeOther }
}

// 标签页滚动
const tagScroll = () => {
    const { getTags } = useLayoutStore()
    const { tagsList, cachedViews } = getTags
    const scrollbar:Ref<{wrap:HTMLElement, update():void} | null> = ref(null)
    const layoutTagsItem:Ref<Array<ComponentInternalInstance | Element | null>> = ref([])
    const getTagsDom = (el:ComponentInternalInstance | Element | null) => el && layoutTagsItem.value.push(el)
    // 监听标签页导航
    watch(
        () => tagsList.length,
        () => nextTick(() => {
            if(!scrollbar.value) return
            scrollbar.value.update()
            nextTick(() => {
                const itemWidth = layoutTagsItem.value.filter(v => v).reduce((acc, v) => {
                    const val = v as HTMLElement
                    return acc + val.offsetWidth + 6
                }, 0)
                if(!scrollbar.value) return
                const scrollLeft = itemWidth - scrollbar.value.wrap.offsetWidth + 70
                if(scrollLeft > 0) scrollbar.value.wrap.scrollLeft = scrollLeft
            })
        })
    )
    // 确保在每次变更之前重置引用
    onBeforeUpdate(() => {
        layoutTagsItem.value = []
    })
    return { tagsList, scrollbar, layoutTagsItem, cachedViews, getTagsDom }
}
export default defineComponent({
    name: 'LayoutTags',
    setup() {
        const { removeAllTagNav, addCachedViews, removeTagNav } = useLayoutStore()
        const route = useRoute()
        const removeTag = (v: any) => removeTagNav({ cPath: route.path, tagsList: v })
        
        onMounted(() => {
            addCachedViews({ name: route.name as string, noCache: route.meta.noCache as boolean })
        })
        
        return {
            removeTag,
            removeAllTagNav,
            ...tagScroll(),
            ...rightMenu()
        }
    }
})
</script>