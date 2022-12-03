<template>
    <div id='dynamicexample'>
        <h2>项目详情</h2>
        <p>项目编码：{{ projName }}</p>
        <el-input v-model='input' />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRoute } from 'vue-router'
export default defineComponent({
    name: 'ProjectDetail',
    setup() {
        const route = useRoute()
        return {
            projName: route.params.projName,
            input: ref('')
        }
    }
})
</script>

