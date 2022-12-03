<template>
    <el-card shadow='hover' class='mb-2'>
        <template #header>
            <div class='card-header flex justify-between items-center'>
                <span>快速开始</span>
            </div>
        </template>
        <div ref='chartDom' class='w-full h-64' />
    </el-card>

    <el-card shadow='hover' class='mb-2'>
        <template #header>
            <div class='card-header flex justify-between items-center'>
                <span>圆饼图</span>
            </div>
        </template>
        <div ref='chartDom2' class='w-full h-64' />
    </el-card>
</template>
<script lang='ts'>
import { defineComponent, onMounted, ref } from 'vue'
import { echarts, ECOption } from '/@/components/Echart'


// 雷达图
const chartRadar:() => ECOption = () => {
    const option:ECOption = {
        title: {
            text: '基础雷达图'
        },
        tooltip: {},
        legend: {
            data: ['预算分配', '实际开销']
        },
        radar: {
            // shape: 'circle',
            axisName: {
                textStyle: {
                    color: '#fff',
                    backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5]
                }
            },
            indicator: [
                { name: '销售', max: 6500 },
                { name: '管理', max: 16000 },
                { name: '信息技术', max: 30000 },
                { name: '客服', max: 38000 },
                { name: '研发', max: 52000 },
                { name: '市场', max: 25000 }
            ]
        },
        series: [{
            name: '预算 vs 开销',
            type: 'radar',
            // areaStyle: {normal: {}},
            data: [
                {
                    value: [4300, 10000, 28000, 35000, 50000, 19000],
                    name: '预算分配'
                },
                {
                    value: [5000, 14000, 28000, 31000, 42000, 21000],
                    name: '实际开销'
                }
            ]
        }]
    }
    return option
}

// 圆饼图
const chartPie:() => ECOption = () => {
    const option:ECOption = {
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '5%',
            left: 'center'
        },
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '40',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    { value: 1048, name: '搜索引擎' },
                    { value: 735, name: '直接访问' },
                    { value: 580, name: '邮件营销' },
                    { value: 484, name: '联盟广告' },
                    { value: 300, name: '视频广告' }
                ]
            }
        ]
    }
    return option
}

// 图标初始化
const chartInit = () => {
    const chartDom = ref(null)
    const chartDom2 = ref(null)
    onMounted(() => {
        const optionsArray:echarts.ECharts[] = []
        let myChart = echarts.init(chartDom.value as unknown as HTMLElement)
        myChart.setOption(chartRadar())
        optionsArray.push(myChart)
        myChart = echarts.init(chartDom2.value as unknown as HTMLElement)
        myChart.setOption(chartPie())
        optionsArray.push(myChart)
        window.onresize = () => {
            optionsArray.forEach(v => v.resize())
        }
    })
    return {
        chartDom,
        chartDom2
    }
}


export default defineComponent({
    setup() {
        
        return {
            ...chartInit()
        }
    }
})
</script>