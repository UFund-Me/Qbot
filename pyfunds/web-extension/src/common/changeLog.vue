<template>
  <el-dialog
    title="更新日志"
    :custom-class="darkMode ? 'changelog darkMode' : 'changelog'"
    :show-close="false"
    :close-on-click-modal="false"
    :modal-append-to-body="false"
    :close-on-press-escape="false"
    :visible.sync="centerDialogVisible"
    :top="top + 'px'"
    width="460px"
    center
  >
    <div v-if="netError" class="btn-row">
      网络不好？
      <el-button type="primary" @click="goGitee">去官网查看</el-button>
    </div>
    <div
      class="content"
      v-show="!netError"
      v-loading="loading"
      :element-loading-background="
        darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
      "
    >
      <p>qq交流群：{{ changelog.qqGroup }}</p>
      <p>
        电报交流群：<a target="_Blank" :href="changelog.tgGroup">点击跳转</a>
      </p>
      <div class="qrcode-row">
        <div class="qrcode-list">
          <p>微信群二维码</p>
          <div ref="qrcode" id="qrcode"></div>
        </div>
        <div class="qrcode-list">
          <p>小程序二维码</p>
          <div class="mpcode">
            <img :src="'./../icons/qrcode/mp.jpg'" />
          </div>
        </div>
      </div>

      <p v-if="changelog.tip">{{ changelog.tip }}</p>
      <div v-if="changelog.htmlTip" v-html="changelog.htmlTip"></div>
      <ul>
        <li v-for="el in changelog.list" :key="el.version">
          <h5>
            v{{ el.version }}
            <span class="btn red" v-if="localVersion == el.version"
              >当前版本</span
            >
            <span class="btn primary" v-if="el.type == 2">重要更新</span>
          </h5>
          <ul>
            <li
              :class="i.type == 2 ? 'major' : ''"
              v-for="(i, ind) in el.content"
              :key="ind"
            >
              {{ i.content }}
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="close">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
var json = require("./changeLog.json");
const { version } = require("../../package.json");
import QRCode from "qrcodejs2";
export default {
  props: {
    top: {
      type: Number,
      default: 0,
    },
    darkMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      updateurl: {
        github: "https://x2rr.github.io/funds/src/common/changeLog.json",
        gitee: "https://rabt.gitee.io/funds/src/common/changeLog.json",
      },
      centerDialogVisible: false,
      qrcode: false,
      changelog: {},
      loading: true,
      netError: false,
      localVersion: version,
    };
  },
  mounted() {},
  methods: {
    goGitee() {
      window.open("http://rabt.gitee.io/funds/docs/dist/index.html#/ChangeLog");
    },
    getChangelog() {
      this.loading = true;
      this.$axios
        .get(this.updateurl.github)
        .then((res) => {
          this.netError = false;
          this.loading = false;
          this.qrlink = res.data.qrcode;
          this.changelog = res.data;
          this.setQrcode();
        })
        .catch((error) => {
          this.netError = true;
        });
    },
    init() {
      this.centerDialogVisible = true;
      this.getChangelog();
    },
    setQrcode() {
      let that = this;
      this.qrcode = new QRCode("qrcode", {
        width: 160,
        height: 160, // 高度
        text: this.changelog.qrcode, // 二维码内容
      });
    },

    close() {
      if (this.qrcode) {
        this.qrcode.clear();
      }
      this.$refs.qrcode.innerHTML = null;
      this.centerDialogVisible = false;

      this.$emit("close", false);
    },
  },
};
</script>

<style lang="scss" scoped>
.changelog {
  /deep/ &.el-dialog {
    margin-bottom: 15px;
    border-radius: 15px;
  }

  .btn-row {
    text-align: center;
    padding: 30px 0;
  }

  #qrcode {
    text-align: center;
    width: 160px;
    height: 160px;
    padding: 6px;
    background-color: #fff;
  }
  .qrcode-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    .qrcode-list {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding-bottom: 10px;
      p {
        padding-bottom: 5px;
      }
    }
    .mpcode {
      width: 172px;
      height: 172px;
      img {
        width: 172px;
        height: 172px;
      }
    }
  }

  .content {
    height: 400px;
    p {
      text-align: center;
      margin: 0;
      padding: 2px 0;
    }

    overflow-y: auto;
    ul {
      padding-left: 22px;
      margin: 5px 0;
      li {
        padding: 3px 0;
        .major {
          font-weight: bold;
        }
        h5 {
          margin: 10px 0;
          font-size: 15px;
          font-weight: bold;
        }
      }
    }
    .btn {
      display: inline-block;
      line-height: 1;
      background: #fff;
      padding: 4px 6px;
      border-radius: 3px;
      font-size: 12px;
      color: #000000;
      margin: 0 3px;
      outline: none;
      border: 1px solid #dcdfe6;
    }
    .primary {
      color: #409eff;
      border-color: #409eff;
    }
  }
  /deep/ &.el-dialog--center .el-dialog__header {
    border-bottom: 1px solid #eee;
    padding: 15px 20px 10px;
  }
  /deep/ &.el-dialog--center .el-dialog__footer {
    border-top: 1px solid #eee;
    padding: 10px 20px 10px;
  }
  /deep/ &.el-dialog--center .el-dialog__body {
    padding: 10px 12px;
  }
}

.changelog.darkMode {
  /deep/ &.el-dialog {
    background-color: #373737;
    .el-dialog__header .el-dialog__title {
      color: rgba($color: #ffffff, $alpha: 0.6);
    }
    .el-dialog__body {
      color: rgba($color: #ffffff, $alpha: 0.6);
    }
  }
  .btn {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.6);
  }
  .btn.red {
    border: 1px solid rgba($color: #f56c6c, $alpha: 0.6);
    background-color: rgba($color: #f56c6c, $alpha: 0.6);
  }

  .primary {
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
    background-color: rgba($color: #409eff, $alpha: 0.6);
  }

  .el-button--primary {
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
    background-color: rgba($color: #409eff, $alpha: 0.6);
    color: rgba($color: #ffffff, $alpha: 0.6);
  }
}
</style>
