<template>
    <el-col :xs='24' :sm='12' :xl='8'>
        <div class='card-list-item flex mb-3 text-sm'>
            <div class='text-right pr-3' :style='{"lineHeight": "28px","width": width, "minWidth": width}'>
                <span v-if='isRequire' class='text-red-600 select-none'>*</span>
                <slot name='key' />
                <span>:</span>
            </div>
            <div class='flex-1 font-semibold' :class='{"truncate": !prop}' :style='{"lineHeight": !prop ? "28px" : "inherit"}'>
                <el-form-item v-if='prop' :prop='prop'>
                    <slot name='value' />
                </el-form-item>
                <slot v-else name='value' />
            </div>
        </div>
    </el-col>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'CardListItem',
    props: {
        width: {
            type: String,
            default: '80px'
        },
        isRequire: {
            type: Boolean,
            default: false
        },
        prop: {
            type: String,
            default: ''
        }
    },
    setup() {
        return {}
    }
})
</script>

    
<style lang='postcss' scoped>

    ::v-deep(.el-select),
    ::v-deep(.el-date-editor.el-input),
    ::v-deep(.el-date-editor.el-input__inner) {
        width: 100%;
    }

    ::v-deep(.el-form-item--mini.el-form-item),
    ::v-deep(.el-form-item--small.el-form-item) {
        margin-bottom: 0;
    }
</style>