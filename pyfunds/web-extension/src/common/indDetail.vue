<template>
  <div v-if="boxShadow" class="shadow" :class="boxClass">
    <div class="content-box">
      <h5>{{ codeData.f14 }}({{ codeData.f13 + "." + codeData.f12 }})</h5>
      <div
        v-loading="loading"
        :element-loading-background="
          darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
        "
        :class="mini ? 'mini-charts' : ''"
        class="main-echarts"
        ref="mainCharts"
      ></div>

      <div class="tab-row">
        <input class="btn" type="button" value="返回列表" @click="close" />
      </div>
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
  name: "indDetail",
  props: {
    mini: {
      type: Boolean,
      default: false,
    },
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
      maxVal: null,
      interVal: null,
      option: {},
      DWJZ: 0,
      code: null,
      codeData: {},
      boxShadow: false,
      loading: false,
      dataList: [],
      timeData: [],
      isHK: false,
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
    boxClass() {
      let className = "";
      if (this.darkMode) {
        className += "darkMode ";
      }
      if (this.mini) {
        className += "mini";
      }
      return className;
    },
  },
  mounted() {
    // this.init();
  },
   beforeDestroy() {
    this.myChart.clear();
  },
  methods: {
    formatNum(val) {
      return (val / 10000).toFixed(3) + "万";
    },
    init(val) {
      this.boxShadow = true;
      this.code = val.f13 + "." + val.f12;
      this.codeData = val;

      setTimeout(() => {
        this.initChart();
      }, 10);
    },
    initChart() {
      this.chartEL = this.$refs.mainCharts;
      this.myChart = echarts.init(
        this.chartEL,
        this.darkMode ? "dark" : "customed"
      );

      this.option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              show: true,
              color: this.defaultColor,
              backgroundColor: this.darkMode
                ? "rgba(0,0,0,0.8)"
                : "rgba(0,0,0,0.6)",
            },
          },
          formatter: (p) => {
            var color;
            if (
              p[0].dataIndex == 0 ||
              this.dataList[p[0].dataIndex][1] >
                this.dataList[p[0].dataIndex - 1][1]
            ) {
              color = '#f56c6c"';
            } else {
              color = '#4eb61b"';
            }
            return `时间：${p[0].name}<br />价格：${
              this.dataList[p[0].dataIndex][1]
            }<br />涨幅：${(
              ((this.dataList[p[0].dataIndex][1] - this.DWJZ) * 100) /
              this.DWJZ
            ).toFixed(
              2
            )}%<br /><span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${color}"></span>成交量：${this.formatNum(
              this.dataList[p[0].dataIndex][2]
            )}`;
          },
        },
        axisPointer: {
          link: { xAxisIndex: "all" },
        },
        grid: [
          {
            top: 20,
            left: 60,
            height: "50%",
          },
          {
            show: true,
            left: 60,
            top: "65%",
            height: "28%", //交易量图的高度
          },
        ],
        xAxis: [
          {
            data: this.timeData,
            position: "bottom",
            axisLine: {
              onZero: false,
            },
          },
          {
            //交易量图
            splitNumber: 2,
            type: "category",
            gridIndex: 1,
            boundaryGap: false,
            data: this.timeData,

            axisTick: {
              show: false,
            },
            splitLine: {
              //分割线设置
              show: true,
              lineStyle: {
                type: "dashed",
                color: this.defaultColor,
              },
            },
            axisLine: {
              lineStyle: {},
            },
            axisPointer: {
              show: true,
              label: {
                formatter: (p) => {
                  if (
                    p.seriesData[0] &&
                    this.dataList[p.seriesData[0].dataIndex]
                  ) {
                    var _p =
                      (
                        this.dataList[p.seriesData[0].dataIndex][2] / 10000
                      ).toFixed(3) + "万";
                    return _p;
                  }
                },
              },
            },
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              color: this.yAxisLabelColor,
              formatter: (val) => {
                return val.toFixed(2);
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
            axisPointer: {
              show: true,
              label: {
                formatter: function(params) {
                  return params.value.toFixed(2);
                },
              },
            },
          },
          {
            type: "value",
            axisLabel: {
              color: this.yAxisLabelColor,
              formatter: (val) => {
                let num = (((val - this.DWJZ) * 100) / this.DWJZ).toFixed(2);
                if (num == -0.00) {
                  num = "0.00";
                }
                return num + "%";
              },
            },
            splitLine: {
              show: true,
              lineStyle: {
                type: "dashed",
                color: this.defaultColor,
              },
            },
            axisPointer: {
              show: true,
              label: {
                formatter: (p) => {
                  return (
                    (((p.value - this.DWJZ) * 100) / this.DWJZ).toFixed(2) + "%"
                  );
                },
              },
            },
            data: [],
          },
          {
            //交易图
            // name: '万',
            nameGap: "0",
            nameTextStyle: {},
            gridIndex: 1,
            z: 4,
            splitNumber: 3,
            axisLine: {
              onZero: false,
              show: false,
            },
            axisTick: {
              show: false,
            },

            splitLine: {
              //分割线设置
              show: false,
            },
            axisPointer: {
              show: true,
              label: {
                formatter: function(params) {
                  var _p = (params.value / 10000).toFixed(2) + "万";
                  return _p;
                },
              },
            },
            axisLabel: {
              //label文字设置
              //   color: labelColor,
              inside: false, //label文字朝内对齐
              fontSize: 10,
              onZero: false,
              formatter: function(params) {
                //计算右边Y轴对应的当前价的涨幅比例
                var _p = (params / 10000).toFixed(2);
                if (params == 0) {
                  _p = "(万)";
                }
                return _p;
              },
            },
          },
        ],
        series: [
          {
            name: "涨幅",
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
            name: "价格",
            type: "line",
            yAxisIndex: 1,
            symbol: "none",
            data: [],
            lineStyle: {
              normal: {
                width: 0,
              },
            },
          },
          {
            name: "成交量",
            type: "bar",
            gridIndex: 1,
            xAxisIndex: 1,
            yAxisIndex: 2,
            data: [],
            itemStyle: {
              normal: {
                color: this.CJcolor,
              },
            },
          },
        ],
      };
      this.getData();
    },

    close() {
      this.boxShadow = false;
      this.$emit("close", false);
    },
    fmtAxis(val, ind) {
      if (this.isHK) {
        if (val == "12:00") {
          return "12:00/13:00";
        } else {
          return val;
        }
      } else {
        if (val == "11:30") {
          return "11:30/13:00";
        } else {
          return val;
        }
      }
    },
    fmtVal(ind, val) {
      var arr;
      if (this.isHK) {
        arr = ["09:30", "12:00", "16:00"];
      } else {
        arr = ["09:30", "10:30", "11:30", "14:00", "15:00"];
      }

      if (arr.indexOf(val) != -1) {
        return true;
      } else {
        return false;
      }
    },
    CJcolor(val, ind) {
      var colorList;
      if (
        val.dataIndex == 0 ||
        this.dataList[val.dataIndex][1] > this.dataList[val.dataIndex - 1][1]
      ) {
        colorList = "#f56c6c";
      } else {
        colorList = "#4eb61b";
      }
      return colorList;
    },
    yAxisLabelColor(val, ind) {
      return Number(val).toFixed(2) > this.DWJZ.toFixed(2)
        ? "#f56c6c"
        : Number(val).toFixed(2) == this.DWJZ.toFixed(2)
        ? this.defaultLabelColor
        : "#4eb61b";
    },
    handle_num(data) {
      var _aa = Math.abs((Math.max.apply(null, data) - this.DWJZ) / this.DWJZ);
      var _bb = Math.abs((Math.min.apply(null, data) - this.DWJZ) / this.DWJZ);
      return _aa > _bb ? _aa : _bb;
    },
    getData() {
      this.loading = true;
      let url = `https://push2.eastmoney.com/api/qt/stock/trends2/get?secid=${this.code}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f53,f56,f58&iscr=0&iscca=0&ndays=1&forcect=1`;

      this.$axios.get(url).then((res) => {
        // console.log(res);
        this.loading = false;
        this.DWJZ = res.data.data.prePrice;
        let dataList = res.data.data.trends.map((item) => item.split(","));
        this.dataList = dataList;

        this.option.series[0].data = dataList.map((item) => +item[1]);
        this.option.series[1].data = dataList.map((item) => +item[1]);
        this.option.series[2].data = dataList.map((item) => +item[2]);

        let firstDate = dataList[0][0].substr(11, 5);
        // console.log(firstDate);
        this.isHK = false;

        if (this.codeData.f13 == 1 || this.codeData.f13 == 0) {
          this.timeData = this.time_arr("hs");
          this.option.xAxis[0].axisLabel = {
            formatter: this.fmtAxis,
            interval: this.fmtVal,
          };
          this.option.xAxis[1].axisLabel = {
            formatter: this.fmtAxis,
            interval: this.fmtVal,
          };
        } else {
          switch (firstDate) {
            case "09:30":
              this.timeData = this.time_arr("hk");
              this.isHK = true;
              this.option.xAxis[0].axisLabel = {
                formatter: this.fmtAxis,
                interval: this.fmtVal,
              };
              this.option.xAxis[1].axisLabel = {
                formatter: this.fmtAxis,
                interval: this.fmtVal,
              };
              break;
            case "21:30":
              this.timeData = this.time_arr("us-s");
              break;
            case "22:30":
              this.timeData = this.time_arr("us-w");
              break;

            default:
              break;
          }
        }

        this.option.xAxis[0].data = this.timeData;
        this.option.xAxis[1].data = this.timeData;

        this.option.series[0].markLine.data[0].yAxis = this.DWJZ;

        let aa = this.handle_num(this.option.series[0].data);

        let minVal = this.DWJZ - this.DWJZ * aa;
        let maxVal = this.DWJZ + this.DWJZ * aa;
        this.option.yAxis[0].min = minVal;
        this.option.yAxis[0].max = maxVal;
        this.option.yAxis[0].interval = Math.abs((this.DWJZ - minVal) / 4);
        this.option.yAxis[1].min = minVal;
        this.option.yAxis[1].max = maxVal;
        this.option.yAxis[1].interval = Math.abs((this.DWJZ - minVal) / 4);
        this.myChart.setOption(this.option);
      });
    },
    time_arr(type) {
      if (type.indexOf("us-s") != -1) {
        //生成美股时间段 夏令时
        var timeArr = new Array();
        timeArr.push("21:30");
        return this.getNextTime("21:30", "04:00", 1, timeArr);
      }
      if (type.indexOf("us-w") != -1) {
        //生成美股时间段
        var timeArr = new Array();
        timeArr.push("22:30");
        return this.getNextTime("22:30", "05:00", 1, timeArr);
      }
      if (type.indexOf("hs") != -1) {
        //生成沪深时间段
        var timeArr = new Array();
        timeArr.push("09:30");
        timeArr.concat(this.getNextTime("09:30", "11:30", 1, timeArr));
        timeArr.concat(this.getNextTime("13:00", "15:00", 1, timeArr));
        return timeArr;
      }
      if (type.indexOf("hk") != -1) {
        //生成港股时间段
        var timeArr = new Array();
        timeArr.push("09:30");
        timeArr.concat(this.getNextTime("09:30", "12:00", 1, timeArr));
        timeArr.concat(this.getNextTime("13:00", "16:00", 1, timeArr));
        return timeArr;
      }
    },
    getNextTime(startTime, endTIme, offset, resultArr) {
      var result = this.addTimeStr(startTime, offset);
      resultArr.push(result);
      if (result == endTIme) {
        return resultArr;
      } else {
        return this.getNextTime(result, endTIme, offset, resultArr);
      }
    },
    addTimeStr(time, num) {
      var hour = time.split(":")[0];
      var mins = Number(time.split(":")[1]);
      var mins_un = parseInt((mins + num) / 60);
      var hour_un = parseInt((Number(hour) + mins_un) / 24);
      if (mins_un > 0) {
        if (hour_un > 0) {
          var tmpVal = ((Number(hour) + mins_un) % 24) + "";
          hour = tmpVal.length > 1 ? tmpVal : "0" + tmpVal; //判断是否是一位
        } else {
          var tmpVal = Number(hour) + mins_un + "";
          hour = tmpVal.length > 1 ? tmpVal : "0" + tmpVal;
        }
        var tmpMinsVal = ((mins + num) % 60) + "";
        mins = tmpMinsVal.length > 1 ? tmpMinsVal : 0 + tmpMinsVal; //分钟数为 取余60的数
      } else {
        var tmpMinsVal = mins + num + "";
        mins = tmpMinsVal.length > 1 ? tmpMinsVal : "0" + tmpMinsVal; //不大于整除60
      }
      return hour + ":" + mins;
    },
  },
};
</script>

<style lang="scss" scoped>
.shadow {
  position: absolute;
  width: 100%;
  height: 100%;
  padding: 20px;
  z-index: 1001;
  box-sizing: border-box;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.7);
}

.content-box {
  background: #ffffff;
  border-radius: 15px;
  padding: 0 10px;
  margin: 0 auto;
  text-align: center;
  line-height: 1;
  vertical-align: middle;
  h5 {
    margin: 0;
    padding: 13px;
  }
}

.mini.shadow {
  padding: 30px;
  z-index: 1000;
}

.btn {
  display: inline-block;
  line-height: 1;
  cursor: pointer;
  background: #fff;
  padding: 5px 6px;
  border-radius: 3px;
  font-size: 12px;
  color: #000000;
  margin: 0 5px;
  outline: none;
  border: 1px solid #dcdfe6;
}

.shadow.darkMode {
  .content-box {
    background-color: #373737;
  }
  .btn {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.6);
  }
}
.tab-row {
  padding: 12px 0;
}
.main-echarts {
  width: 100%;
  height: 330px;
}
.mini-charts {
  height: 305px;
}
</style>
