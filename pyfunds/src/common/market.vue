<template>
  <div v-if="boxShadow" class="shadow" :class="darkMode ? 'darkMode' : ''">
    <div class="content-box">
      <h5>行情中心</h5>
      <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick">
        <el-tab-pane lazy label="大盘资金" name="first">
          <market-line :darkMode="darkMode" ref="first"></market-line>
        </el-tab-pane>
        <el-tab-pane lazy label="行业板块" name="second">
          <market-bar :darkMode="darkMode" ref="second"></market-bar>
        </el-tab-pane>
        <el-tab-pane lazy label="北向资金" name="third">
          <market-S2N :darkMode="darkMode" ref="third"></market-S2N>
        </el-tab-pane>
        <el-tab-pane lazy label="南向资金" name="fourth">
          <market-N2S :darkMode="darkMode" ref="fourth"></market-N2S>
        </el-tab-pane>
      </el-tabs>

      <div class="tab-row">
        <input class="btn" type="button" value="返回列表" @click="close" />
      </div>
    </div>
  </div>
</template>

<script>
import marketLine from "./marketLine";
import marketBar from "./marketBar";
import marketS2N from "./marketS2N";
import marketN2S from "./marketN2S";
// import charts2 from "./charts2";
export default {
  components: {
    marketLine,
    marketBar,
    marketS2N,
    marketN2S,
  },
  name: "market",
  props: {
    darkMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      activeName: "first",
      boxShadow: false,
    };
  },
  watch: {},
  mounted() {},
  methods: {
    handleClick(tab, event) {
      this.activeName = tab.name;
    },
    init() {
      this.boxShadow = true;
    },
    close() {
      this.boxShadow = false;
      this.$emit("close", false);
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
  max-width: 600px;
  background: #ffffff;
  border-radius: 15px;
  padding: 0 10px;
  margin: 0 auto;
  text-align: center;
  line-height: 1;
  vertical-align: middle;
  position: relative;
  h5 {
    margin: 0;
    padding: 13px;
  }
  /deep/ .el-tabs__item {
    padding: 0 15px;
    height: 34px;
    line-height: 34px;
  }
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
.tab-row {
  padding: 12px 0;
}
.tab-row:after,
.tab-row:before {
  display: table;
  content: "";
}
.tab-row:after {
  clear: both;
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
  /deep/ .el-tabs--border-card {
    background-color: #373737;
    border: 1px solid rgba($color: #ffffff, $alpha: 0.37);
    .el-tabs__header {
      background-color: rgba($color: #ffffff, $alpha: 0.16);
      border-bottom: 1px solid rgba($color: #ffffff, $alpha: 0.37);
      .el-tabs__item.is-active {
        background-color: rgba($color: #409eff, $alpha: 0.6);
        color: rgba($color: #ffffff, $alpha: 0.6);
        border-right-color: rgba($color: #ffffff, $alpha: 0.37);
        border-left-color: rgba($color: #ffffff, $alpha: 0.37);
      }
    }
  }
  /deep/ .el-radio-button--mini .el-radio-button__inner {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.37);
  }
  /deep/ .el-radio-button__orig-radio:checked + .el-radio-button__inner {
    background-color: rgba($color: #409eff, $alpha: 0.6);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border-color: rgba($color: #409eff, $alpha: 0.37);
  }
}
</style>
