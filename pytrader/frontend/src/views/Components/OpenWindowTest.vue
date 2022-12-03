<template>
    <div class='content'>
        <el-button @click='show = true'>打开窗体</el-button>
        <open-window v-model:show='show' :is-show='show' title='选择页'>
            <p style='height: 1500px;'>aaa</p>
            <template #btn>
                <el-button>默认按钮</el-button>
                <el-button>默认按钮</el-button>
                <el-button>默认按钮</el-button>
            </template>
        </open-window>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import OpenWindow from '/@/components/OpenWindow/index.vue'
export default defineComponent({
    name: 'OpenWindowTest',
    components: {
        OpenWindow
    },
    setup() {
        const show = ref(false)

        return {
            show
        }
    }
})
</script>