<template>
    <transition name='el-fade-in'>
        <div v-if='isShow' class='open-select-mask w-full h-full bg-black bg-opacity-30 z-50 fixed top-0 left-0 flex flex-center'>
            <div class='open-select w-11/12 max-w-screen-xl h-5/6 bg-white flex flex-col overflow-x-hidden overflow-y-auto'>
                <div class='h-10 flex justify-between items-center px-3 shadow-sm border-b border-gray-100'>
                    <span>{{ title }}</span>
                    <div>
                        <i class='el-icon-close cursor-pointer' @click='close' />
                    </div>
                </div>
                <div class='flex-1 overflow-hidden'>
                    <el-scrollbar>
                        <slot name='default' />
                    </el-scrollbar>
                </div>
                <div v-if='slots.btn' class='open-select-btn h-12 flex border-t border-gray-100'>
                    <slot name='btn' />
                </div>
            </div>
        </div>
    </transition>
</template>

<script lang="ts">
import { defineComponent, SetupContext } from 'vue'
export default defineComponent({
    name: 'SelectPage',
    props: {
        isShow: {
            type: Boolean,
            default: false
        },
        title: {
            type: String,
            default: '新窗口'
        }
    },
    emits: ['update:show'],
    setup(props, context: SetupContext) {
        const close = () => context.emit('update:show', !props.isShow)
        return {
            close,
            slots: context.slots
        }
    }
})
</script>

<style lang="postcss" scoped>
    ::v-deep(.open-select-btn .el-button) {
        border-radius: 0;
        flex: 1;

        & + .el-button {
            margin-left: -1px;
        }

        &:hover {
            z-index: 1;
        }
    }

</style>
    