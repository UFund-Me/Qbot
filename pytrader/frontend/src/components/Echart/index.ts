import * as echarts from 'echarts/core'
import {
    BarChart,
    // 系列类型的定义后缀都为 SeriesOption
    BarSeriesOption,
    LineChart,
    RadarChart,
    PieChart,
    PieSeriesOption,
    RadarSeriesOption,
    LineSeriesOption
} from 'echarts/charts'
import {
    TitleComponent,
    TooltipComponent,
    RadarComponent,
    GridComponent,
    LegendComponent,
    // 组件类型的定义后缀都为 ComponentOption
    TitleComponentOption,
    GridComponentOption,
    LegendComponentOption
} from 'echarts/components'
import {
    CanvasRenderer
} from 'echarts/renderers'

// 通过 ComposeOption 来组合出一个只有必须组件和图表的 Option 类型
type ECOption = echarts.ComposeOption<
  BarSeriesOption | LineSeriesOption | TitleComponentOption | GridComponentOption | RadarSeriesOption | PieSeriesOption | LegendComponentOption
>;

// 注册必须的组件
echarts.use(
    [TitleComponent, TooltipComponent, GridComponent, BarChart, LineChart, RadarChart, RadarComponent, PieChart, CanvasRenderer, LegendComponent]
)

export {
    ECOption,
    echarts
}