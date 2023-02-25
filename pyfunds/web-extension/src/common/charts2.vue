<template>
  <div
    class="box"
    v-loading="loading"
    :element-loading-background="
      darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
    "
  >
    <div class="main-echarts" ref="mainCharts"></div>
    <div>
      <el-radio-group v-model="sltTimeRange" @change="changeTimeRange">
        <el-radio-button label="y">月</el-radio-button>
        <el-radio-button label="3y">季</el-radio-button>
        <el-radio-button label="6y">半年</el-radio-button>
        <el-radio-button label="n">一年</el-radio-button>
        <el-radio-button label="3n">三年</el-radio-button>
        <el-radio-button label="5n">五年</el-radio-button>
      </el-radio-group>
    </div>
  </div>
</template>

<script>
let echarts = require("echarts/lib/echarts");

import "./js/customed.js";
import "./js/dark.js";

require("echarts/lib/chart/line");

require("echarts/lib/component/tooltip");
require("echarts/lib/component/legend");

export default {
  name: "chatrs",
  props: {
    darkMode: {
      type: Boolean,
      default: false,
    },
    fund: {
      type: Object,
      required: true,
    },
    chartType: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      chartEL: null,
      myChart: null,
      minVal: null,
      maxVal: null,
      interVal: null,
      sltTimeRange: "y",
      chartTypeList: {
        DWJZ: {
          name: "单位净值",
        },
        LJJZ: {
          name: "累计净值",
        },
      },
      option: {},
      loading: false,
    };
  },

  watch: {},
  computed: {
    defaultColor() {
      return this.darkMode ? "rgba(255,255,255,0.6)" : "#ccc";
    },
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {
    this.myChart.clear();
  },
  methods: {
    init() {
      this.chartEL = this.$refs.mainCharts;
      this.myChart = echarts.init(
        this.chartEL,
        this.darkMode ? "dark" : "customed"
      );
      this.option = {
        tooltip: {
          trigger: "axis",
          formatter: (p) => {
            return `时间：${p[0].name}<br />${
              this.chartTypeList[this.chartType].name
            }：${p[0].value}`;
          },
        },
        grid: {
          top: 30,
          bottom: 30,
          left: 60
        },
        xAxis: {
          type: "category",
          data: [],
          axisLabel: {},
        },
        yAxis: {
          type: "value",
          scale: true,
          axisLabel: {
            color: this.defaultColor,
            formatter: (val) => {
              if (this.chartType == "LJSY") {
                return val.toFixed(1) + "%";
              } else {
                return val.toFixed(3);
              }
            },
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: "dashed",
              color: this.defaultColor,
            },
          },
          data: [],
        },
        series: [
          {
            type: "line",
            data: [],
          },
        ],
      };
      this.getData();
    },
    changeTimeRange(val) {
      this.getData();
    },
    handle_num_range(data) {
      var _aa = Math.max.apply(null, data);
      var _bb = Math.min.apply(null, data);
      return [_aa, _bb];
    },
    getData() {
      this.loading = true;
      if (this.chartType == "LJSY") {
        let url = `https://fundmobapi.eastmoney.com/FundMApi/FundYieldDiagramNew.ashx?FCODE=${
          this.fund.fundcode
        }&RANGE=${
          this.sltTimeRange
        }&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&_=${new Date().getTime()}`;
        this.$axios.get(url).then((res) => {
          this.loading = false;
          let dataList = res.data.Datas;
          if (dataList) {
            this.option.legend = {
              show: true,
            };
            this.option.tooltip.formatter = (p) => {
              let str =
                p.length > 1 ? `<br />${p[1].seriesName}：${p[1].value}%` : "";
              return `时间：${p[0].name}<br />${p[0].seriesName}：${p[0].value}%${str}`;
            };
            this.option.series = [
              {
                type: "line",
                name: "涨幅",
                data: dataList.map((item) => +item.YIELD),
              },
              {
                type: "line",
                name: res.data.Expansion.INDEXNAME,
                data: dataList.map((item) => +item.INDEXYIED),
              },
            ];
            this.option.xAxis.data = dataList.map((item) => item.PDATE);
            this.myChart.setOption(this.option);
          }
        });
      } else {
        let url = `https://fundmobapi.eastmoney.com/FundMApi/FundNetDiagram.ashx?FCODE=${
          this.fund.fundcode
        }&RANGE=${
          this.sltTimeRange
        }&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&_=${new Date().getTime()}`;
        this.$axios.get(url).then((res) => {
          this.loading = false;
          let dataList = res.data.Datas;
          this.option.series = [
            {
              type: "line",
              name: "单位净值",
              data: dataList.map((item) => +item.DWJZ),
            },
            {
              type: "line",
              name: "累计净值",
              data: dataList.map((item) => +item.LJJZ),
            },
          ];
          this.option.tooltip.formatter = (p) => {
            let str =
              p.length > 1 ? `<br />${p[1].seriesName}：${p[1].value}` : "";
            return `时间：${p[0].name}<br />${p[0].seriesName}：${
              p[0].value
            }${str}<br />日增长率：${dataList[p[0].dataIndex].JZZZL}%`;
          };
          this.option.legend = {
            show: true,
          };
          this.option.xAxis.data = dataList.map((item) => item.FSRQ);
          this.myChart.setOption(this.option);
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.box {
  width: 100%;
  height: 100%;
}
.main-echarts {
  width: 100%;
  height: 232px;
}
</style>
