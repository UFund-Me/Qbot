<script lang="ts">
import { defineComponent, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
export default defineComponent({
    name: 'Redirect',
    setup() {
        const route = useRoute()
        const router = useRouter()
        const { pathMatch } = route.params
        router.replace({ path: typeof pathMatch === 'string' ? `/${pathMatch}` : `/${pathMatch.join('/')}` })
    },
    render() {
        return h('div')
    }
})
</script>