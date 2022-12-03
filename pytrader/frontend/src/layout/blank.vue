<template>
    <div>
        <router-view />
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'LayoutBlank',
    setup() {
        return {}
    }
})
</script>