<template>
  <div
    class="box"
    v-loading="loading"
    :element-loading-background="
      darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
    "
  >
    <div class="main-echarts" ref="mainCharts"></div>
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
  name: "marketBar",
  props: {
    darkMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      chartEL: null,
      myChart: null,
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
            return `${p[0].name}<br />${(p[0].value/100000000).toFixed(2)}亿元`;
          },
        },
        grid: {
          top: 30,
          bottom: 110,
          right: 30,
        },
        xAxis: {
          type: "category",
          data: [],
          axisLabel: {
            formatter: (value) => {
              return value.split("").join("\n");
            },
          },
        },
        yAxis: {
          type: "value",
          name: "单位：亿元",
          scale: true,
          axisLabel: {
            color: this.defaultColor,
            formatter: (val) => {
              return (val / 100000000).toFixed(2);
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
        dataZoom: [
          {
            type: "slider",
            show: true,
            xAxisIndex: [0],
            start: 0,
            end: 30,
          },
          {
            type: "inside",
            xAxisIndex: [0],
            start: 1,
            end: 30,
          },
        ],
        series: [
          {
            type: "bar",
            data: [],
          },
        ],
      };
      this.getData();
    },

    getData() {
      this.loading = true;
      let url = `http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f12,f13,f14,f62&fid=f62&fs=m:90+t:2&_=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        this.loading = false;
        let dataList = res.data.data.diff;
        let xdata = [];
        let sdata = [];

        if (dataList) {
          dataList.forEach((el) => {
            xdata.push(el.f14);
            sdata.push(el.f62);
          });

          this.option.xAxis.data = xdata;

          this.option.series = [
            {
              type: "bar",
              data: sdata,
              itemStyle: {
                normal: {
                  color: function(data) {
                    return data.value >= 0 ? "#f56c6c" : "#4eb61b";
                  },
                },
              },
            },
          ];
          this.myChart.setOption(this.option);
        }
      });
    },
    fmtAxis(val, ind) {
      if (val == "11:30") {
        return "11:30/13:00";
      } else {
        return val;
      }
    },
    fmtVal(ind, val) {
      let arr = ["09:30", "10:30", "11:30", "14:00", "15:00"];
      if (arr.indexOf(val) != -1) {
        return true;
      } else {
        return false;
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
  height: 260px;
}
</style>
