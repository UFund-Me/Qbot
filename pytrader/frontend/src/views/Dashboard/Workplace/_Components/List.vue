<template>
    <!-- <list type='card' :data='list'>
        <template #header>
            <div class='card-header flex justify-between items-center'>
                <span>我的关注</span>
                <el-link
                    type='primary'
                    :underline='false'
                    href='javascript:;'
                >全部</el-link>
            </div>
        </template>
    </list> -->
    <el-card shadow='hover' class='mb-2'>
        <template #header>
            <div class='card-header flex justify-between items-center'>
                <span>关注</span>
                <div>
                    <el-link
                        type='primary'
                        :underline='false'
                        href='javascript:;'
                        @click='loadStocks'
                    >
                        刷新</el-link>
                    <el-link
                        type='primary'
                        :underline='false'
                        href='javascript:;'
                        @click='addNewStock'
                    >
                        添加</el-link>
                </div>
            </div>
        </template>
        <el-table :data='stocks' border style='width: 100%;'>
            <el-table-column fixed prop='name' label='名称' />
            <el-table-column prop='code' label='代码' sortable />
            <el-table-column prop='now' label='当前价格' sortable />
            <el-table-column label='涨跌幅' width='180' sortable>
                <template #default='scope'>
                    <div style='display: flex; align-items: center'>
                        <span style='margin-left: 10px' :class='addClass(scope.row)'>{{ scope.row['now'] - scope.row['open'] > 0 ? "+":"" }}{{ (scope.row['now'] - scope.row['open']).toFixed(2) }} ({{ scope.row['涨跌(%)'] }}%)</span>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label='做T价格' width='180'>
                <template #default='scope'>
                    <div style='display: flex; align-items: center'>
                        <span style='margin-left: 10px'>卖1：{{ scope.row['t_price'][0].toFixed(2) }}<br>卖2：{{ scope.row['t_price'][1].toFixed(2) }}<br>买1：{{ scope.row['t_price'][2].toFixed(2) }}<br>买2：{{ scope.row['t_price'][3].toFixed(2) }}</span>
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop='成交量(手)' label='成交量（手)' sortable />
            <el-table-column prop='总市值' label='总市值' sortable />
            <el-table-column prop='市盈(静)' label='市盈(静)' sortable />
            <el-table-column fixed='right' label=''>
                <template #default='scope'>
                    <el-button type='text' size='small' @click='remove(scope.row.code)'>删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
    
    <el-dialog
        v-model='show'
        title='新增关注股票'
        width='30%'
        :before-close='handleClose'
    >
        <el-form ref='ruleForm' label-position='right' label-width='80px' :rules='rules'>
            <el-form-item class='mb-6 -ml-20' prop='code'>
                <el-input v-model='newStock' maxlength='6' minlength='6' placeholder='请输入股票代码' prefix-icon='el-icon-user' />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class='dialog-footer'>
                <el-button @click='show = false'>取消</el-button>
                <el-button
                    type='primary'
                    @click='addWatchStock'
                >添加</el-button>
            </span>
        </template>
    </el-dialog>
        
    <!-- <el-card shadow='hover' class='mb-2'>
        <template #header>
            <div class='card-header flex justify-between items-center'>
                <span>预警</span>
            </div>
        </template>
        <list :data='list'>
            <template #default='scope'>
                <el-button @click='edit(scope.item)'>查看</el-button>
            </template>
        </list>
    </el-card> -->
</template>
<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'
import { IList } from '/@/components/List/index.vue'
import { addStock, getStocks, IStocks, removeWatchStock } from '/@/api/layout/index'
import { ElNotification, ElMessageBox, ElMessage } from 'element-plus'
// import OpenWindow from '/@/components/OpenWindow/index.vue'

let autoReloadTimer:any = null

export default defineComponent({
    components: {
        // OpenWindow
    },
    setup() {
        const rules = reactive({
            code: [
                {
                    required: true,
                    message: '请输入股票代码',
                    trigger: 'blur'
                },
                {
                    min: 6,
                    max: 6,
                    message: '股票代码为6位',
                    trigger: 'blur'
                }
            ]
        })
        const stocks = ref<IStocks[]>([])
        const newStock = ref<string>('')
        const show = ref(false)
        const loadStocks = async() => {
            const res = await getStocks()
            stocks.value = res.data
        }

        const addWatchStock = async() => {
            const res = await addStock(newStock.value)
            if (res.data.data) {
                ElNotification({
                    title: '提示',
                    message: '添加成功'
                })
                show.value = false
                newStock.value = ''
                loadStocks()
            } else {
                ElNotification({
                    title: '提示',
                    message: '添加失败'
                })
            }
        }

        const remove = async(code:string) => {
            ElMessageBox.confirm(
                `确认删除关注股票${code}`,
                'Warning',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }
            )
                .then(async() => {
                    const res = await removeWatchStock(code)
                    if (res.data.data) {
                        ElMessage({
                            type: 'success',
                            message: 'Delete completed'
                        })
                        loadStocks()
                    } else {
                        ElNotification({
                            title: '提示',
                            message: '删除失败'
                        })
                    } 
                })
                .catch(() => {
                    ElMessage({
                        type: 'info',
                        message: 'Delete canceled'
                    })
                })
        }


        return {
            edit: (item: IList) => console.log(item),
            show,
            stocks,
            newStock,
            rules,
            remove,
            loadStocks,
            addWatchStock,
            addNewStock: () => {
                show.value = true
            },
            addClass : (row: any) => {
                return row['涨跌(%)'] > 0 ? 'cell-red' : 'cell-green'
            }
        }
    },
    mounted() {
        this.loadStocks()
        // autoReloadTimer = window.setInterval(this.loadStocks, 5000)
    },
    unmounted() {
        clearInterval(autoReloadTimer)
    }
})
</script>

<style lang='postcss' scoped>

.cell-red {
    color: red;
}

.cell-green{
    color: green;
}

.el-link {
  margin-right: 8px;
}

.el-link .el-icon--right.el-icon {
  vertical-align: text-bottom;
}

</style>