<template>
  <div v-if="boxShadow" class="shadow" :class="darkMode ? 'darkMode' : ''">
    <div class="content-box">
      <h5>{{ fund.name }}({{ fund.fundcode }})</h5>
      <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick">
        <el-tab-pane lazy label="净值估算" name="first">
          <charts :darkMode="darkMode" :fund="fund" ref="first"></charts>
        </el-tab-pane>
        <el-tab-pane lazy label="持仓明细" name="ccmx">
          <position-detail
            :darkMode="darkMode"
            @sltStock="sltStock"
            :fund="fund"
          >
          </position-detail>
        </el-tab-pane>
        <el-tab-pane lazy label="历史净值" name="second">
          <charts2
            :darkMode="darkMode"
            :fund="fund"
            chartType="JZ"
            ref="second"
          ></charts2>
        </el-tab-pane>
        <el-tab-pane lazy label="累计收益" name="third">
          <charts2
            :darkMode="darkMode"
            :fund="fund"
            chartType="LJSY"
            ref="third"
          ></charts2>
        </el-tab-pane>
        <el-tab-pane lazy label="基金概况" name="info">
          <fund-info
            :darkMode="darkMode"
            :fund="fund"
            ref="info"
            @showManager="showManager"
          ></fund-info>
        </el-tab-pane>
      </el-tabs>

      <div class="tab-row">
        <input class="btn" type="button" value="返回列表" @click="close" />
      </div>
    </div>
    <ind-detail mini ref="indDetail" :darkMode="darkMode"> </ind-detail>
    <manager-detail ref="managerDetail" :darkMode="darkMode"> </manager-detail>
  </div>
</template>

<script>
import charts from "./charts";
import charts2 from "./charts2";
import positionDetail from "./positionDetail";
import indDetail from "../common/indDetail";
import fundInfo from "../common/fundInfo";
import managerDetail from "../common/managerDetail";
export default {
  components: {
    charts,
    charts2,
    positionDetail,
    indDetail,
    fundInfo,
    managerDetail,
  },
  name: "fundDetail",
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
    showManager(val) {
      this.$refs.managerDetail.init(val);
    },
    sltStock(val) {
      this.$refs.indDetail.init(val);
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
  box-sizing: border-box;
  z-index: 1001;
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
