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
      <ul class="chart-list">
        <li>
          沪股通 当日净流入 <span
            :class="lastDataList[1] >= 0 ? 'red' : 'green'"
            >{{ (lastDataList[1] / 10000).toFixed(2) }} 亿元</span
          ><span>，当日余额 </span
          ><span :class="lastDataList[2] >= 0 ? 'red' : 'green'"
            >{{ (lastDataList[2] / 10000).toFixed(2) }} 亿元</span
          >
        </li>
        <li>
          深股通 当日净流入 <span
            :class="lastDataList[3] >= 0 ? 'red' : 'green'"
            >{{ (lastDataList[3] / 10000).toFixed(2) }} 亿元</span
          ><span>，当日余额 </span
          ><span :class="lastDataList[4] >= 0 ? 'red' : 'green'"
            >{{ (lastDataList[4] / 10000).toFixed(2) }} 亿元</span
          >
        </li>
        <li>
          北向资金 当日净流入 <span
            :class="lastDataList[5] >= 0 ? 'red' : 'green'"
            >{{ (lastDataList[5] / 10000).toFixed(2) }} 亿元</span
          >
        </li>
      </ul>
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
  name: "marketS2N",
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
      minVal: null,
      option: {},
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
      lastDataList: [0, 0, 0, 0, 0, 0],
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
          // formatter: (p) => {
          //   return `时间：${p[0].name}<br />${
          //     this.chartTypeList[this.chartType].name
          //   }：${p[0].value}`;
          // },
        },
        grid: {
          top: 55,
          bottom: 30,
          right: 30,
        },
        xAxis: {
          type: "category",
          data: this.timeData,
          axisLabel: {
            formatter: this.fmtAxis,
            interval: this.fmtVal,
          },
          axisLine: {
            onZero: false,
          },
        },
        yAxis: {
          type: "value",
          name: "单位：亿元",
          scale: true,
          axisLabel: {
            color: this.defaultColor,
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
    getData() {
      this.loading = true;
      let url = `http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&ut=&?v=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        this.loading = false;
        let data = res.data.data;
        // console.log(data.s2nDate, data.s2n);

        let dataList = data.s2n;
        let data1 = [];
        let data3 = [];
        let data5 = [];

        if (dataList) {
          dataList.forEach((el) => {
            let arr = el.split(",");

            if (arr[1] != "-") {
              this.lastDataList = arr;
            }

            data1.push((arr[1] / 10000).toFixed(4));
            data3.push((arr[3] / 10000).toFixed(4));
            data5.push((arr[5] / 10000).toFixed(4));
          });
          this.option.legend = {
            show: true,
          };
          this.option.series = [
            {
              type: "line",
              name: "沪股通",
              data: data1,
            },
            {
              type: "line",
              name: "深股通",
              data: data3,
            },
            {
              type: "line",
              name: "北向资金",
              data: data5,
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
  height: 206px;
}

.chart-list {
  text-align: left;
  margin: 0 auto;
  width: 90%;
}

li {
  line-height: 18px;
}
.green {
  color: #4eb61b;
}
.red {
  color: #f56c6c;
}
</style>
