import { mount, VueWrapper } from '@vue/test-utils'
import { nextTick, ComponentPublicInstance, ref } from 'vue'
import CardList from '/@/components/CardList/CardList.vue'
import CardListItem from '/@/components/CardList/CardListItem.vue'
import ElementPlus from 'element-plus'

describe('CardList.vue', () => {
    const createCardList = function(props:string, opts:IObject<any> | null, slot?:string): VueWrapper<ComponentPublicInstance> {
        return mount(Object.assign({
            components: {
                CardList,
                CardListItem
            },
            template: `
                <card-list
                    ${props}
                >${slot}</card-list>
            `
        }, opts), {
            global: {
                plugins: [ElementPlus]
            }
        })
    }
    const listItem = ref([
        { text: '标题标题标题标题标题标题标题标题标题标题', mark: '2020/12/21', url: 'http://baidu.com', target: '_blank' },
        { text: '标题标题标题标题标题标题标题标题标题标题', mark: '2020/12/21' },
        { text: '标题标题标题标题标题标题标题标题标题标题', mark: '2020/12/21' }
    ])
    it('show title', async() => {
        const wrapper: VueWrapper<ComponentPublicInstance> = createCardList(
            ':list-item="listItem" :show-header="true" title="显示标题"',
            {
                setup() {
                    return { listItem }
                }
            }
        )
        await nextTick()
        expect(wrapper.find('.card-list .el-card__header>div>span').text()).toEqual('显示标题')
    })
    it('hide liststyle', async() => {
        const wrapper: VueWrapper<ComponentPublicInstance> = createCardList(
            ':list-item="listItem" :show-liststyle="false"',
            {
                setup() {
                    return { listItem }
                }
            }
        )
        await nextTick()
        expect(wrapper.find('.card-list .card-list-body .card-list-item-circle').exists()).toBe(false)
    })
    it('wrap', async() => {
        const wrapper: VueWrapper<ComponentPublicInstance> = createCardList(
            ':list-item="listItem" :is-nowrap="false"',
            {
                setup() {
                    return { listItem }
                }
            }
        )
        await nextTick()
        expect(wrapper.find('.card-list .card-list-body .card-list-text').classes()).toContain('wrap')
    })
    it('hide liststyle', async() => {
        const wrapper: VueWrapper<ComponentPublicInstance> = createCardList(
            ':list-item="listItem" :show-liststyle="false"',
            {
                setup() {
                    return { listItem }
                }
            }
        )
        await nextTick()
        expect(wrapper.find('.card-list .card-list-body .card-list-item-circle').exists()).toBe(false)
    })
    it('keyvalue', async() => {
        const wrapper: VueWrapper<ComponentPublicInstance> = createCardList(
            'type="keyvalue"',
            {
                setup() {
                    return { }
                }
            },
            `
            <template #keyvalue>
                <card-list-item>
                    <template #key>
                        申请单号
                    </template>
                    <template #value>
                        2020001686
                    </template>
                </card-list-item>
            </template>
            `
        )
        await nextTick()
        expect(wrapper.find('.card-list .card-list-item .text-right span').text()).toEqual(':')
        expect(wrapper.find('.card-list .card-list-item .font-semibold.truncate').text()).toEqual('2020001686')
    })
})