<template>
    <div>
        <p style='height: 1500px;'>高度超出，滚动条测试</p>
        <span>aa</span>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
export default defineComponent({
    name: 'ProjectImport',
    setup() {
        const input = ref('')
        return {
            input
        }
    }
})
</script>

