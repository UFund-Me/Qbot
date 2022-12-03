<template>
    <div v-if='type==="default"'>
        <div v-for='(val,index) in data' :key='index' class='py-2 border-b hover:bg-gray-100'>
            <div class='flex justify-between items-center'>
                <div class='flex items-center'>
                    <div v-if='val.imgUrl || val.iconClass' class='mr-4'>
                        <el-avatar v-if='val.imgUrl' size='large' :src='val.imgUrl' />
                        <i v-if='val.iconClass' :class='{"text-3xl": true, [val.iconClass]: true}' />
                    </div>
                    <div>
                        <el-link v-if='val.href' type='primary' :underline='false' :href='val.href'>
                            <p class='text-sm mb-1'>
                                {{ val.subTitle }}
                                <el-tag v-if='val.tag'>{{ val.tag }}</el-tag>
                            </p>
                        </el-link>
                        <p v-else class='text-sm mb-1'>
                            {{ val.subTitle }}
                            <el-tag v-if='val.tag'>{{ val.tag }}</el-tag>
                        </p>
                        <p v-if='val.time' class='text-xs text-gray-500'>{{ val.time }}</p>
                    </div>
                </div>
                <slot :item='val' />
            </div>
        </div>
    </div>

    <div v-if='type==="card"' class='component-list-card'>
        <el-card shadow='never' class='mb-2'>
            <template #header>
                <slot name='header' />
            </template>
            <el-row>
                <el-col v-for='(val,index) in data' :key='index' :xs='24' :sm='12' :md='8' class='c-list-card-body h-40 text-sm text-gray-400'>
                    <div v-if='val.title' class='flex items-center py-1 text-black font-medium'>
                        <div>
                            <el-avatar v-if='val.imgUrl' size='small' :src='val.imgUrl' />
                            <i v-if='val.iconClass' :class='{"text-3xl": true, [val.iconClass]: true}' />
                        </div>
                        <div class='px-4 truncate text-base'>{{ val.title }}</div>
                    </div>
                    <div class='py-1 h-16 overflow-ellipsis overflow-hidden leading-6'>
                        <el-link v-if='val.href' type='primary' :underline='false' :href='val.href'>
                            <p class='text-sm mb-1'>{{ val.subTitle }}</p>
                        </el-link>
                        <p v-else>{{ val.subTitle }}</p>
                    </div>
                    <div class='flex items-center justify-between'>
                        <div>{{ val.tag }}</div>
                        <div>{{ val.time }}</div>
                    </div>
                </el-col>
            </el-row>
        </el-card>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export interface IList {
    imgUrl?: string
    iconClass?: string
    title?: string
    subTitle?: string
    href?:string
    tag?:string
    time?:string
}

export type IListType = 'default' | 'card'

export default defineComponent({
    name: 'List',
    props: {
        data: {
            type: Array as PropType<Array<IList>>,
            default: () => []
        },
        type: {
            type: String as PropType<IListType>,
            default: 'default'
        }
    },
    setup() {
        return {}
    }
})
</script>

<style lang='postcss' scoped>
    ::v-deep(.el-card__header) {
        margin-bottom: -1px;
    }

    ::v-deep(.el-card__body) {
        padding: 0;
    }

    .c-list-card-body {
        transition: all 0.3s;
        position: relative;
        padding: 15px;
        box-shadow: 1px 0 0 0 #f0f0f0, 0 1px 0 0 #f0f0f0, 1px 1px 0 0 #f0f0f0, inset 1px 0 0 0 #f0f0f0, inset 0 1px 0 0 #f0f0f0;
    }

    .c-list-card-body:hover {
        z-index: 1;
        box-shadow: 0 2px 12px 0 rgb(0 0 0 / 10%);
    }
</style>