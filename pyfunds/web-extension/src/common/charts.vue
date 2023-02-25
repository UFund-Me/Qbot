<template>
  <div
    v-loading="loading"
    :element-loading-background="
      darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
    "
    class="main-echarts"
    ref="mainCharts"
  ></div>
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
  },
  data() {
    return {
      chartEL: null,
      myChart: null,
      minVal: null,
      maxVal: null,
      interVal: null,
      option: {},
      DWJZ: 0,
      loading: false,
      timeData: [
        "09:30",
        "09:31",
        "09:32",
        "09:33",
        "09:34",
        "09:35",
        "09:36",
        "09:37",
        "09:38",
        "09:39",
        "09:40",
        "09:41",
        "09:42",
        "09:43",
        "09:44",
        "09:45",
        "09:46",
        "09:47",
        "09:48",
        "09:49",
        "09:50",
        "09:51",
        "09:52",
        "09:53",
        "09:54",
        "09:55",
        "09:56",
        "09:57",
        "09:58",
        "09:59",
        "10:00",
        "10:01",
        "10:02",
        "10:03",
        "10:04",
        "10:05",
        "10:06",
        "10:07",
        "10:08",
        "10:09",
        "10:10",
        "10:11",
        "10:12",
        "10:13",
        "10:14",
        "10:15",
        "10:16",
        "10:17",
        "10:18",
        "10:19",
        "10:20",
        "10:21",
        "10:22",
        "10:23",
        "10:24",
        "10:25",
        "10:26",
        "10:27",
        "10:28",
        "10:29",
        "10:30",
        "10:31",
        "10:32",
        "10:33",
        "10:34",
        "10:35",
        "10:36",
        "10:37",
        "10:38",
        "10:39",
        "10:40",
        "10:41",
        "10:42",
        "10:43",
        "10:44",
        "10:45",
        "10:46",
        "10:47",
        "10:48",
        "10:49",
        "10:50",
        "10:51",
        "10:52",
        "10:53",
        "10:54",
        "10:55",
        "10:56",
        "10:57",
        "10:58",
        "10:59",
        "11:00",
        "11:01",
        "11:02",
        "11:03",
        "11:04",
        "11:05",
        "11:06",
        "11:07",
        "11:08",
        "11:09",
        "11:10",
        "11:11",
        "11:12",
        "11:13",
        "11:14",
        "11:15",
        "11:16",
        "11:17",
        "11:18",
        "11:19",
        "11:20",
        "11:21",
        "11:22",
        "11:23",
        "11:24",
        "11:25",
        "11:26",
        "11:27",
        "11:28",
        "11:29",
        "11:30",
        "13:00",
        "13:01",
        "13:02",
        "13:03",
        "13:04",
        "13:05",
        "13:06",
        "13:07",
        "13:08",
        "13:09",
        "13:10",
        "13:11",
        "13:12",
        "13:13",
        "13:14",
        "13:15",
        "13:16",
        "13:17",
        "13:18",
        "13:19",
        "13:20",
        "13:21",
        "13:22",
        "13:23",
        "13:24",
        "13:25",
        "13:26",
        "13:27",
        "13:28",
        "13:29",
        "13:30",
        "13:31",
        "13:32",
        "13:33",
        "13:34",
        "13:35",
        "13:36",
        "13:37",
        "13:38",
        "13:39",
        "13:40",
        "13:41",
        "13:42",
        "13:43",
        "13:44",
        "13:45",
        "13:46",
        "13:47",
        "13:48",
        "13:49",
        "13:50",
        "13:51",
        "13:52",
        "13:53",
        "13:54",
        "13:55",
        "13:56",
        "13:57",
        "13:58",
        "13:59",
        "14:00",
        "14:01",
        "14:02",
        "14:03",
        "14:04",
        "14:05",
        "14:06",
        "14:07",
        "14:08",
        "14:09",
        "14:10",
        "14:11",
        "14:12",
        "14:13",
        "14:14",
        "14:15",
        "14:16",
        "14:17",
        "14:18",
        "14:19",
        "14:20",
        "14:21",
        "14:22",
        "14:23",
        "14:24",
        "14:25",
        "14:26",
        "14:27",
        "14:28",
        "14:29",
        "14:30",
        "14:31",
        "14:32",
        "14:33",
        "14:34",
        "14:35",
        "14:36",
        "14:37",
        "14:38",
        "14:39",
        "14:40",
        "14:41",
        "14:42",
        "14:43",
        "14:44",
        "14:45",
        "14:46",
        "14:47",
        "14:48",
        "14:49",
        "14:50",
        "14:51",
        "14:52",
        "14:53",
        "14:54",
        "14:55",
        "14:56",
        "14:57",
        "14:58",
        "14:59",
        "15:00",
      ],
    };
  },
  watch: {},
  computed: {
    defaultColor() {
      return this.darkMode ? "rgba(255,255,255,0.6)" : "#ccc";
    },
    defaultLabelColor() {
      return this.darkMode ? "rgba(255,255,255,0.6)" : "#000";
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
            return `时间：${p[0].name}<br />估算涨跌幅：${
              p[0].value
            }%<br />估算净值：${(this.DWJZ * (1 + 0.01 * p[0].value)).toFixed(
              4
            )}元`;
          },
        },
        grid: {
          top: 30,
          bottom: 30,
        },
        xAxis: {
          type: "category",
          data: this.timeData,
          position: "bottom",
          axisLabel: {
            formatter: this.fmtAxis,
            interval: this.fmtVal,
          },
          axisLine: {
            onZero: false,
          },
        },
        yAxis: [
          {
            type: "value",
            axisLabel: {
              color: this.yAxisLabelColor,
              formatter: (val) => {
                return val.toFixed(2) + "%";
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
          {
            type: "value",
            axisLabel: {
              color: this.yAxisLabelColor,
              formatter: (val) => {
                return (this.DWJZ * (1 + 0.01 * val)).toFixed(4);
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
        ],
        series: [
          {
            name: "估算涨跌幅",
            type: "line",
            data: [],
            markLine: {
              silent: true,
              symbol: "none",
              animation: false,
              label: {
                show: false,
              },
              lineStyle: {
                type: "solid",
              },
              data: [
                {
                  yAxis: 0,
                },
              ],
            },
          },
          {
            name: "估算净值",
            type: "line",
            symbol: "none",
            data: [],
            yAxisIndex: 1,
            lineStyle: {
              normal: {
                width: 0,
              },
            },
          },
        ],
      };
      this.getData();
    },

    fmtAxis(val, ind) {
      if (val == "13:00") {
        return "11:30/13:00";
      } else {
        return val;
      }
    },
    fmtVal(ind, val) {
      let arr = ["09:30", "10:30", "13:00", "14:00", "15:00"];
      if (arr.indexOf(val) != -1) {
        return true;
      } else {
        return false;
      }
    },
    yAxisLabelColor(val, ind) {
      return val > 0
        ? "#f56c6c"
        : val == 0
        ? this.defaultLabelColor
        : "#4eb61b";
    },
    handle_num(data) {
      var _aa = Math.abs(Math.max.apply(null, data)).toFixed(2);
      var _bb = Math.abs(Math.min.apply(null, data)).toFixed(2);
      return _aa > _bb ? _aa : _bb;
    },
    getData() {
      this.loading = true;
      let url = `https://fundmobapi.eastmoney.com/FundMApi/FundVarietieValuationDetail.ashx?FCODE=${
        this.fund.fundcode
      }&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&_=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        this.loading = false;
        let dataList = res.data.Datas.map((item) => item.split(","));
        this.option.series[0].data = dataList.map((item) =>
          (+item[2]).toFixed(2)
        );
        this.option.series[1].data = dataList.map((item) =>
          (+item[2]).toFixed(2)
        );
        let aa = this.handle_num(this.option.series[0].data);
        this.DWJZ = res.data.Expansion.DWJZ;
        this.option.yAxis[0].min = -aa;
        this.option.yAxis[0].max = aa;
        this.option.yAxis[0].interval = aa / 4;
        this.option.yAxis[1].min = -aa;
        this.option.yAxis[1].max = aa;
        this.option.yAxis[1].interval = aa / 4;
        this.myChart.setOption(this.option);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.main-echarts {
  width: 100%;
  height: 260px;
}
</style>
