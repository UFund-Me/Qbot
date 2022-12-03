<template>
  <div
    class="box"
    v-loading="loading"
    :element-loading-background="
      darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
    "
  >
    <h5>
      <span v-if="expansion">截止日期：{{ expansion }}</span>
      <span v-else>暂无数据</span>
    </h5>
    <table>
      <thead>
        <tr>
          <th style="text-align: left;">股票名称（代码）</th>
          <th>价格</th>
          <th>涨跌幅</th>
          <th>持仓占比</th>
          <th>较上期</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(el, ind) in dataList" :key="el.GPDM" @click="openPage(ind)">
          <td class="gpcode" style="text-align: left;">
            {{ el.GPJC + "（" + el.GPDM + "）" }}
          </td>
          <td>{{ dataListGp[ind].f2.toFixed(2) }}</td>
          <td :class="dataListGp[ind].f3 >= 0 ? 'up' : 'down'">
            {{ dataListGp[ind].f3.toFixed(2) }}%
          </td>
          <td>{{ parseFloat(el.JZBL).toFixed(2) }}%</td>
          <td>{{ compared(el) }}</td>
        </tr>
      </tbody>
    </table>
    
  </div>
</template>

<script>
// import indDetail from "../common/indDetail";
export default {
  components: {
    // indDetail,
  },
  name: "positionDetails",
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
      dataList: [],
      dataListGp: [],
      expansion: null,
      loading: false,
      sltData:{}
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
  methods: {
    init() {
      this.getData();
    },

    getData() {
      this.loading = true;
      let url = `https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition?FCODE=${
        this.fund.fundcode
      }&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        let dataList = res.data.Datas.fundStocks;
        if (dataList) {
          let gpList = dataList
            .map((val) => {
              return val.NEWTEXCH + "." + val.GPDM;
            })
            .join(",");

          let gpUrl = `https://push2.eastmoney.com/api/qt/ulist.np/get?fields=f1,f2,f3,f4,f12,f13,f14,f292&fltt=2&secids=${gpList}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=`;
          this.$axios.get(gpUrl).then((resGp) => {
            this.loading = false;
            this.dataListGp = resGp.data.data.diff;
            this.dataList = dataList;
            this.expansion = res.data.Expansion;
          });
        } else {
          this.loading = false;
        }
      });
    },
    openPage(ind) {
      let val = this.dataListGp[ind];
      this.sltData = val;
      this.$emit("sltStock", val);

      // let url = `https://emwap.eastmoney.com/quota/stock/index/${val.GPDM}${val.TEXCH}`;
      // window.open(url);
    },

    compared(val) {
      if (val.PCTNVCHGTYPE == "新增") {
        return "新增";
      } else if (isNaN(val.PCTNVCHG)) {
        return 0;
      } else {
        let icon = val.PCTNVCHG > 0 ? "↑ " : "↓ ";
        return icon + Math.abs(parseFloat(val.PCTNVCHG)).toFixed(2) + "%";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.box {
  width: 100%;
  height: 100%;
  min-height: 260px;
  h5 {
    margin: 0;
    padding: 0 0 6px;
  }
}
table {
  border-collapse: collapse;
  width: 100%;
  th,
  td {
    text-align: right;
    line-height: 22px;
    height: 22px;
    padding: 0 8px;
  }
  tr {
    &:nth-child(even) {
      background-color: #f1f1f1;
    }
  }
}

.gpcode:hover {
  color: #409eff;
  cursor: pointer;
}

.darkMode table tr:nth-child(even) {
  background-color: rgba($color: #ffffff, $alpha: 0.05);
}
.up {
  color: #f56c6c;
  font-weight: bold;
}

.down {
  color: #4eb61b;
  font-weight: bold;
}
</style>
