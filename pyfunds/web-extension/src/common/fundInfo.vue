<template>
  <div
    class="box"
    v-loading="loading"
    :element-loading-background="
      darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
    "
  >
    <div v-if="infoData.FCODE" class="content-box">
      <div class="hisrank-row">
        <div>
          <div>近1月(排名)</div>
          <p :class="infoData.SYL_Y > 0 ? 'up' : 'down'">
            {{ infoData.SYL_Y }}%（{{ infoData.RANKM }}）
          </p>
        </div>
        <div>
          <div>近3月(排名)</div>
          <p :class="infoData.SYL_3Y > 0 ? 'up' : 'down'">
            {{ infoData.SYL_3Y }}%（{{ infoData.RANKQ }}）
          </p>
        </div>
        <div>
          <div>近6月(排名)</div>
          <p :class="infoData.SYL_6Y > 0 ? 'up' : 'down'">
            {{ infoData.SYL_6Y }}%（{{ infoData.RANKHY }}）
          </p>
        </div>
        <div>
          <div>近1年(排名)</div>
          <p :class="infoData.SYL_1N > 0 ? 'up' : 'down'">
            {{ infoData.SYL_1N }}%（{{ infoData.RANKY }}）
          </p>
        </div>
      </div>
      <div>单位净值：{{ infoData.DWJZ }}（{{ infoData.FSRQ }}）</div>
      <div>累计净值：{{ infoData.LJJZ }}</div>
      <div>基金类型：{{ infoData.FTYPE }}</div>
      <div>基金公司：{{ infoData.JJGS }}</div>
      <div class="hover" @click="showManager">
        基金经理：{{ infoData.JJJL }}
      </div>
      <div>交易状态：{{ infoData.SGZT }} {{ infoData.SHZT }}</div>
      <div>基金规模：{{ numberFormat(infoData.ENDNAV) }}</div>
      <div v-if="infoData.FUNDBONUS">
        分红状态：{{ infoData.FUNDBONUS.PDATE }}日，每份基金份额折算{{
          infoData.FUNDBONUS.CHGRATIO
        }}份
      </div>
    </div>
    
  </div>
</template>

<script>
// import indDetail from "../common/indDetail";
export default {
  components: {
    // indDetail,
  },
  name: "fundInfo",
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
      infoData: {},
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
  methods: {
    init() {
      this.getData();
    },

    getData() {
      this.loading = true;
      let url = `https://fundmobapi.eastmoney.com/FundMApi/FundBaseTypeInformation.ashx?FCODE=${
        this.fund.fundcode
      }&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        this.loading = false;
        this.infoData = res.data.Datas;
        // let dataList = res.data.Datas.fundStocks;
      });
    },
    
    numberFormat(value) {
      var param = {};
      var k = 10000,
        sizes = ["", "万", "亿", "万亿"],
        i;
      if (value < k) {
        param.value = value;
        param.unit = "";
      } else {
        i = Math.floor(Math.log(value) / Math.log(k));

        param.value = (value / Math.pow(k, i)).toFixed(2);
        param.unit = sizes[i];
      }
      return param.value + param.unit;
    },
    showManager() {
      this.$emit("showManager", this.fund.fundcode);
    },
    close() {
      this.boxShadow = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.box {
  width: 100%;
  height: 100%;
  min-height: 260px;
}
.content-box {
  text-align: left;
  & > div {
    padding: 0 20px;
    line-height: 26px;
    &:nth-child(even) {
      background-color: #f1f1f1;
    }
  }

  .hisrank-row {
    display: flex;
    justify-content: space-between;
    padding: 0 10px;
    & > div {
      text-align: center;
      margin: 0 10px;
      
      p {
        margin: 0;
      }
    }
  }
}

.hover:hover {
  color: #409eff;
  cursor: pointer;
}

.up {
  color: #f56c6c;
  font-weight: bold;
}

.down {
  color: #4eb61b;
  font-weight: bold;
}

.darkMode .content-box > div:nth-child(even) {
  background-color: rgba($color: #ffffff, $alpha: 0.05);
}

.shadow {
  position: absolute;
  width: 100%;
  height: 100%;
  padding: 30px;
  z-index: 1001;
  box-sizing: border-box;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.7);
}

.manager-box {
  background: #ffffff;
  border-radius: 15px;
  padding: 0 10px;
  margin: 0 auto;
  text-align: center;
  line-height: 1;
  vertical-align: middle;
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
  .manager-box {
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

.manager-content {
  width: 100%;
  height: 305px;
}
</style>
