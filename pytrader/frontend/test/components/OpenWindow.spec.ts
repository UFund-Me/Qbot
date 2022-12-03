import { mount, VueWrapper } from '@vue/test-utils'
import { nextTick, ComponentPublicInstance, ref } from 'vue'
import OpenWindow from '/@/components/OpenWindow/index.vue'
import ElementPlus from 'element-plus'

describe('OpenWindow.vue', () => {
    const wrapper: VueWrapper<ComponentPublicInstance> = mount({
        components: {
            OpenWindow
        },
        template: `
            <div class='content'>
                <el-button @click='show = true'>
                    打开窗体
                </el-button>
                <open-window
                    v-model:show='show'
                    :is-show='show'
                    title='选择页'
                >
                    <p style='height: 1500px;'>
                        aaa
                    </p>
                    <template #btn>
                        <el-button>
                            默认按钮
                        </el-button>
                        <el-button>
                            默认按钮
                        </el-button>
                        <el-button>
                            默认按钮
                        </el-button>
                    </template>
                </open-window>
            </div>
            `,
        setup() {
            const show = ref(false)
        
            return {
                show
            }
        }
    }, {
        global: {
            plugins: [ElementPlus]
        }
    })
    it('hide', async() => {
        await nextTick()
        expect(wrapper.find('.open-select').exists()).toBe(false)
    })
    it('click show', async() => {
        await nextTick()
        const btn = wrapper.find('.content .el-button')
        btn.trigger('click')
        await nextTick()
        expect(wrapper.find('.open-select').exists()).toBe(true)
    })
    
    it('attr title', async() => {
        await nextTick()
        const btn = wrapper.find('.content .el-button')
        btn.trigger('click')
        await nextTick()
        expect(wrapper.find('.open-select>div>span').text()).toEqual('选择页')
    })
})