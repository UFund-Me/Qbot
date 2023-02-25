<template>
  <div id="app" class="container" :class="containerClass">
    <div>
      <ul class="setting-list">
        <li>
          <div class="list-title">
            角标展示设置
          </div>
          <div class="select-row">
            角标开关：
            <el-radio-group
              v-model="showBadge"
              @change="changeOption($event, 'showBadge', true)"
            >
              <el-radio border :label="1">打开角标</el-radio>
              <el-radio border :label="2">关闭角标</el-radio>
            </el-radio-group>
          </div>
          <div v-if="showBadge == 1" class="select-row">
            角标内容：
            <el-radio-group
              v-model="BadgeContent"
              @change="changeOption($event, 'BadgeContent', true)"
            >
              <el-radio border :label="1">单个基金</el-radio>
              <el-radio border :label="2">所有基金</el-radio>
              <el-radio border :label="3">单个指数</el-radio>
            </el-radio-group>
          </div>
          <div v-if="showBadge == 1 && BadgeContent != 3" class="select-row">
            角标类型：
            <el-radio-group
              v-model="BadgeType"
              @change="changeOption($event, 'BadgeType', true)"
            >
              <el-radio border :label="1">日收益率</el-radio>
              <el-radio border :label="2">日收益额</el-radio>
            </el-radio-group>
          </div>
          <p style="margin-top:5px">
            tips：若选择单个基金，请打开编辑按钮中的特别关注选项；若要计算收益额，需要先打开显示持有金额开关，在编辑中填写基金对应的持有额。
          </p>
        </li>
        <li>
          <div class="list-title">
            主题与页面设置
          </div>
          <div class="select-row">
            <el-switch
              v-model="darkMode"
              @change="changeDarkMode"
              active-color="#484848"
              inactive-color="#13ce66"
              inactive-text="标准模式"
              active-text="暗色模式"
            >
            </el-switch>
          </div>
          <div class="select-row">
            <el-switch
              v-model="normalFontSize"
              @change="changeFontSize"
              inactive-text="迷你字号"
              active-text="标准字号"
            >
            </el-switch>
          </div>
        </li>

        <li>
          <div class="list-title">
            基金列表展示内容设置
          </div>
          <div class="select-row">
            <span>显示估算净值</span>
            <el-switch
              v-model="showGSZ"
              @change="changeOption($event, 'showGSZ')"
            >
            </el-switch>
          </div>
          <div class="select-row">
            <span>显示持有金额</span>
            <el-switch
              v-model="showAmount"
              @change="changeOption($event, 'showAmount')"
            >
            </el-switch>
          </div>
          <div class="select-row">
            <span>显示估值收益</span>
            <el-switch
              v-model="showGains"
              @change="changeOption($event, 'showGains')"
            >
            </el-switch>
          </div>
          <div class="select-row">
            <span>显示持有收益</span>
            <el-switch
              v-model="showCost"
              @change="changeOption($event, 'showCost')"
            >
            </el-switch>
          </div>
          <div class="select-row">
            <span>显示持有收益率</span>
            <el-switch
              v-model="showCostRate"
              @change="changeOption($event, 'showCostRate')"
            >
            </el-switch>
          </div>
          <p>
            tips：在编辑设置里，输入持有份额可计算当日估值收益。输入持仓成本可计算累计持有收益。
          </p>
        </li>
        <li>
          <div class="list-title">
            基金配置信息导入与导出
          </div>
          <div style="padding:8px 0 10px">
            <input
              class="btn"
              type="button"
              value="导出配置文件"
              @click="exportConfig"
            />
            <a
              class="exportBtn"
              ref="configMsg"
              :href="configHref"
              download="自选基金助手配置文件.json"
            ></a>
            <a href="javascript:;" class="uploadFile btn"
              >导入配置文件
              <input
                ref="importInput"
                type="file"
                accept="application/json"
                @change="importInput"
              />
            </a>
            <input
              class="btn"
              type="button"
              value="导入导出文本"
              @click="openConfigBox"
            />
          </div>
          <div style="padding:8px 0 10px">
            <input
              class="btn"
              type="button"
              value="导出基金列表Excel"
              :disabled="loadingFundList"
              @click="getFundData"
            />
            <a href="javascript:;" class="uploadFile btn"
              >导入基金列表Excel
              <input
                ref="importExcel"
                type="file"
                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
                @change="importExcel"
              />
            </a>
          </div>
          <p>
            tips：插件本身支持跟随浏览器账号自动同步，若想手动同步可使用导入导出功能，同步小程序数据可以选择导入导出文本，Excel导入时不用填写基金名称。
          </p>
        </li>
        <li>
          <div class="list-title">请作者喝杯咖啡</div>
          <p style="line-height:34px">
            开源不易，本插件是一个完全开源的项目，也衍生出许多同类产品，您的支持是对作者最大的鼓励。如果你觉得此插件对你有所帮助，或者想要支持一下我<input
              class="btn primary"
              type="button"
              title="φ(>ω<*)"
              value="点击打赏"
              @click="reward"
            />
          </p>
          <p style="line-height:34px">
            或者你也可以帮忙点一个star，点击查看源码→
            <span
              title="点击查看项目源码"
              class="black icon-btn-row"
              @click="openGithub"
            >
              <svg
                class="githubIcon"
                height="24"
                viewBox="0 0 16 16"
                version="1.1"
                width="24"
                aria-hidden="true"
              >
                <path
                  d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
                />
              </svg>
              <input
                class="btn black githubText"
                type="button"
                value="源代码"
              />
            </span>
          </p>
          <reward :top="50" ref="reward"></reward>
        </li>
        <li>
          <div class="list-title">
            节假日信息
            <button
              :disabled="disabled"
              @click="getHoliday"
              title="点击更新节假日信息"
              class="btn"
            >
              更新
            </button>
            <span class="loading" v-if="disabled">更新中。。。</span>
          </div>
          <p>
            <span v-if="holiday">
              当前节假日版本：v{{
                holiday.version
              }}&nbsp;&nbsp;&nbsp;&nbsp;最后节假日日期：{{ holiday.lastDate }}
            </span>
          </p>
          <p>
            tips：更新节假日信息，可以在节假日暂停更新估值，节假日信息会不定时更新。
            <a href="#" @click="openHoliday">查看最新版</a>
          </p>
        </li>
        <li>
          <div class="list-title">
            关于插件
          </div>
          <p style="line-height:34px">
            当前插件版本：v{{ version }}
            <input
              class="btn"
              type="button"
              value="更新日志"
              @click="changelog"
            />
            <input
              class="btn"
              type="button"
              value="插件主页"
              @click="openHomePage"
            />
          </p>
          <p style="line-height:34px">
            电报群：https://t.me/choose_funds_chat
            <input class="btn" type="button" value="点击跳转" @click="openTG" />
          </p>
          <change-log
            @close="closeChangelog"
            :darkMode="darkMode"
            ref="changelog"
            :top="20"
          ></change-log>
          <config-box
            @success="successInput"
            :darkMode="darkMode"
            ref="configBox"
            :top="40"
          >
          </config-box>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import reward from "../common/reward";
import changeLog from "../common/changeLog";
import configBox from "../common/configBox";
const { version } = require("../../package.json");
import { export_json_to_excel } from "../common/js/vendor/Export2Excel";
export default {
  components: {
    reward,
    changeLog,
    configBox,
  },
  data() {
    return {
      fundListM: null,
      userId: null,
      configHref: null,
      holiday: null,
      disabled: false,
      showGSZ: false,
      showAmount: false,
      showGains: false,
      showCost: false,
      showCostRate: false,
      darkMode: false,
      showBadge: 1,
      BadgeContent: 1,
      BadgeType: 1,
      changelogShadow: false,
      normalFontSize: false,
      loadingFundList: false,
      version,
    };
  },
  mounted() {
    this.initOption();
  },
  watch: {},
  computed: {
    containerClass() {
      if (this.darkMode) {
        return "darkMode";
      }
    },
  },
  methods: {
    getFundData() {
      this.loadingFundList = true;
      this.$message({
        message: "正在导出中，请稍候......",
        type: "success",
        center: true,
      });
      let fundlist = this.fundListM.map((val) => val.code).join(",");
      let url =
        "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo?pageIndex=1&pageSize=200&plat=Android&appType=ttjj&product=EFund&Version=1&deviceid=" +
        this.userId +
        "&Fcodes=" +
        fundlist;
      this.$axios
        .get(url)
        .then((res) => {
          let data = res.data.Datas;
          this.dataList = [];
          let dataList = [];

          data.forEach((val) => {
            let data = {
              code: val.FCODE,
              name: val.SHORTNAME,
            };

            let slt = this.fundListM.filter((item) => item.code == data.code);
            data.num = slt[0].num;
            data.cost = slt[0].cost;

            dataList.push(data);
          });
          this.dataList = dataList;
          this.downloadData();
          this.loadingFundList = false;
        })
        .catch((error) => {});
    },
    downloadData() {
      var tHeader = ["基金代码", "基金名称", "持有份额", "成本价"];
      var filterVal = ["code", "name", "num", "cost"];
      var data = this.formatJson(filterVal, this.dataList);
      export_json_to_excel(tHeader, data, "自选基金助手-基金配置");
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) => filterVal.map((j) => v[j]));
    },
    importExcel(e) {
      var files = e.target.files;
      let fileReader = new FileReader();
      fileReader.onload = (event) => {
        try {
          let data = event.target.result;
          let workbook = XLSX.read(data, {
            type: "binary",
          });
          // excel读取出的数据
          let excelData = XLSX.utils.sheet_to_json(
            workbook.Sheets[workbook.SheetNames[0]]
          );
          // 将上面数据转换成 table需要的数据
          let arr = [];
          excelData.forEach((item) => {
            let obj = {};
            obj.code = item["基金代码"];
            obj.num = item["持有份额"];
            obj.cost = item["成本价"];
            arr.push(obj);
          });
          chrome.storage.sync.set({ fundListM: arr }, (val) => {
            this.initOption();
            chrome.runtime.sendMessage({ type: "refresh" });
            this.$message({
              message: "恭喜,导入基金列表成功！",
              type: "success",
              center: true,
            });
            this.$refs.importExcel.value = null;
          });
        } catch (e) {
          this.$message({
            message: "导入失败！",
            type: "error",
            center: true,
          });
          return false;
        }
      };
      // 读取文件 成功后执行上面的回调函数
      fileReader.readAsBinaryString(files[0]);
    },

    changelog() {
      this.changelogShadow = true;
      this.$refs.changelog.init();
    },
    closeChangelog() {
      this.changelogShadow = false;
    },
    changeOption(val, type, sendMessage) {
      chrome.storage.sync.set(
        {
          [type]: val,
        },
        () => {
          this[type] = val;
          if (sendMessage) {
            chrome.runtime.sendMessage({
              type: "refreshOption",
              data: { type: type, value: val },
            });
          }
        }
      );
    },
    initOption() {
      chrome.storage.sync.get(
        [
          "holiday",
          "showNum",
          "showAmount",
          "showGains",
          "showCost",
          "showCostRate",
          "showGSZ",
          "darkMode",
          "normalFontSize",
          "showBadge",
          "BadgeContent",
          "BadgeType",
          "userId",
          "fundListM",
        ],
        (res) => {
          if (res.showNum) {
            //解决版本遗留问题，拆分属性
            chrome.storage.sync.set({
              showNum: false,
            });
            chrome.storage.sync.set(
              {
                showAmount: true,
              },
              () => {
                this.showAmount = true;
              }
            );
            chrome.storage.sync.set(
              {
                showGains: true,
              },
              () => {
                this.showGains = true;
              }
            );
          } else {
            this.showAmount = res.showAmount ? res.showAmount : false;
            this.showGains = res.showGains ? res.showGains : false;
          }

          if (res.holiday) {
            this.holiday = res.holiday;
            console.log(this.holiday);
          } else {
            this.getHoliday();
          }
          if (res.userId) {
            this.userId = res.userId;
          } else {
            this.userId = this.getGuid();
            chrome.storage.sync.set({
              userId: this.userId,
            });
          }
          this.fundListM = res.fundListM ? res.fundListM : [];
          this.showGSZ = res.showGSZ ? res.showGSZ : false;
          this.showCost = res.showCost ? res.showCost : false;
          this.showCostRate = res.showCostRate ? res.showCostRate : false;
          this.darkMode = res.darkMode ? res.darkMode : false;
          this.normalFontSize = res.normalFontSize ? res.normalFontSize : false;
          this.showBadge = res.showBadge ? res.showBadge : 1;
          this.BadgeContent = res.BadgeContent ? res.BadgeContent : 1;
          this.BadgeType = res.BadgeType ? res.BadgeType : 1;
        }
      );
    },
    exportConfig() {
      chrome.storage.sync.get(null, (res) => {
        delete res.holiday;
        this.configHref = "data:text/plain," + JSON.stringify(res);
        setTimeout(() => {
          this.$refs["configMsg"].click();
        }, 200);
      });
    },
    importInput(e) {
      let files = e.target.files;
      if (!files || !files.length) {
        throw new Error("No files");
      }

      let reader = new FileReader();
      reader.onload = (event) => {
        try {
          let config = JSON.parse(event.target.result);
          chrome.storage.sync.set(config, (val) => {
            this.initOption();
            chrome.runtime.sendMessage({ type: "refresh" });
            this.$message({
              message: "恭喜,导入配置成功！",
              type: "success",
              center: true,
            });
            this.$refs.importInput.value = null;
          });
        } catch (e) {
          this.$message({
            message: "导入失败！",
            type: "error",
            center: true,
          });
        }
      };
      reader.readAsText(files[0]);
    },
    successInput() {
      this.initOption();
      chrome.runtime.sendMessage({ type: "refresh" });
    },
    openConfigBox() {
      this.$refs.configBox.init();
    },
    getHoliday() {
      this.disabled = true;
      let url = "https://x2rr.github.io/funds/holiday.json";
      this.$axios.get(url).then((res) => {
        chrome.storage.sync.set(
          {
            holiday: res.data,
          },
          () => {
            this.holiday = res.data;
            chrome.runtime.sendMessage({
              type: "refreshHoliday",
              data: res.data,
            });
            this.disabled = false;
          }
        );
      });
    },
    openHoliday() {
      window.open("https://x2rr.github.io/funds/holiday.json");
    },
    openGithub() {
      window.open("https://github.com/x2rr/funds");
    },
    openTG() {
      window.open("https://t.me/choose_funds_chat");
    },
    openHomePage() {
      window.open("http://rabt.gitee.io/funds/docs/dist/index.html");
    },
    reward(data) {
      this.$refs.reward.init();
    },
    changeDarkMode() {
      chrome.storage.sync.set({
        darkMode: this.darkMode,
      });
    },
    changeFontSize() {
      chrome.storage.sync.set({
        normalFontSize: this.normalFontSize,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  min-width: 630px;
  min-height: 520px;
  text-align: center;
  padding: 15px 0;
  font-size: 13px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.setting-list {
  width: 600px;
  margin: 0 auto;
  text-align: left;
  padding: 0 10px 10px;
  border-radius: 8px;
}

.setting-list li {
  list-style: none;
  font-size: 16px;
  border-bottom: 1px solid #dddddd;
  padding: 10px 0;
}

.setting-list li p {
  margin: 0;
  font-size: 14px;
  color: #999999;
}

.list-title {
  min-height: 34px;
  line-height: 34px;
  font-weight: bold;
}

.select-row {
  line-height: 35px;
  padding-left: 20px;
  & > span {
    display: inline-block;
    width: 120px;
    margin-right: 3px;
    text-align: right;
  }
  input,
  label {
    cursor: pointer;
  }

  .el-radio {
    margin-right: 0;
  }
}

.btn {
  display: inline-block;
  line-height: 1;
  cursor: pointer;
  background: #fff;
  padding: 6px 8px;
  border-radius: 3px;
  font-size: 14px;
  color: #000000;
  margin: 0 5px;
  outline: none;
  border: 1px solid #dcdfe6;
}

.exportBtn {
  visibility: hidden;
}

.uploadFile {
  text-decoration: none;
  display: inline-flex;
  position: relative;
  overflow: hidden;
}

.uploadFile input {
  position: absolute;
  font-size: 100px;
  cursor: pointer;
  right: 0;
  top: 0;
  opacity: 0;
}

.btn[disabled] {
  color: #aaaaaa;
}

.icon-btn-row {
  position: relative;
  cursor: pointer;
}

.githubIcon {
  position: absolute;
  top: -4px;
  left: 12px;
}
.githubText {
  padding-left: 30px;
  padding: 8px 8px 8px 36px;
}

.tips {
  font-size: 12px;
  margin: 0;
  color: #aaaaaa;
  line-height: 1.4;
  padding: 5px 15px;
}
.primary {
  color: #409eff;
  border-color: #409eff;
}

.black {
  color: #24292e;
  border-color: #24292e;
}

//暗黑主题
.container.darkMode {
  color: rgba($color: #ffffff, $alpha: 0.6);
  background-color: #121212;
  .btn {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.6);
  }
  .primary {
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
    background-color: rgba($color: #409eff, $alpha: 0.6);
  }

  .setting-list {
    background-color: rgba($color: #ffffff, $alpha: 0.11);
  }

  .setting-list li {
    border-bottom: 1px solid rgba($color: #ffffff, $alpha: 0.38);
  }

  /deep/ .el-switch__label.is-active {
    color: rgba($color: #409eff, $alpha: 0.87);
  }
  /deep/ .el-switch__label {
    color: rgba($color: #ffffff, $alpha: 0.6);
  }

  /deep/ .el-switch.is-checked .el-switch__core {
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
    background-color: rgba($color: #409eff, $alpha: 0.6);
  }

  /deep/ .el-radio__input.is-checked + .el-radio__label {
    color: rgba($color: #409eff, $alpha: 0.87);
  }
  /deep/ .el-radio__input.is-checked .el-radio__inner {
    background-color: rgba($color: #409eff, $alpha: 0.6);
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
  }
  /deep/ .el-radio.is-bordered.is-checked {
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
  }
  /deep/ .el-radio.is-bordered {
    border: 1px solid rgba($color: #ffffff, $alpha: 0.6);
  }
  /deep/ .el-radio {
    color: rgba($color: #ffffff, $alpha: 0.6);
  }
}
</style>
