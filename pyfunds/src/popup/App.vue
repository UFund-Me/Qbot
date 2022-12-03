<template>
  <div
    id="app"
    class="container"
    ref="app"
    :class="containerClass"
    :style="[zoom, grayscale, opacity]"
  >
    <div>
      <div
        class="tab-row"
        v-if="isGetStorage"
        v-loading="loadingInd"
        :element-loading-background="
          darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
        "
        :style="seciList.length > 0 ? { minHeight: '55px' } : {}"
      >
        <div
          v-for="(el, index) in indFundData"
          :draggable="isEdit"
          class="tab-col indFund"
          :class="drag"
          :key="el.f12"
          @click.stop="!isEdit && indDetail(el)"
          @dragstart="handleDragStart($event, el)"
          @dragover.prevent="handleDragOver($event, el)"
          @dragenter="handleDragEnter($event, el, index)"
          @dragend="handleDragEnd($event, el)"
        >
          <h5>
            {{ el.f14 }}
            <span
              v-if="isEdit"
              @click="dltIndFund(index)"
              class="dltBtn edit red btn"
              >✖</span
            >
          </h5>
          <p :class="el.f3 >= 0 ? 'up' : 'down'">
            {{ el.f2
            }}<input
              v-if="isEdit && BadgeContent == 3"
              @click="sltInd(el)"
              :class="el.f13 + '.' + el.f12 == RealtimeIndcode ? 'slt' : ''"
              class="btn edit"
              style="margin-left:5px"
              value="✔"
              type="button"
            />
          </p>
          <p :class="el.f3 >= 0 ? 'up' : 'down'">
            {{ el.f4 }}&nbsp;&nbsp;{{ el.f3 }}%
          </p>
        </div>
        <div v-if="isEdit && indFundData.length < 4" class="tab-col">
          <div
            v-if="!showAddSeciInput"
            class="addSeci"
            @click="() => (showAddSeciInput = true)"
          >
            添加
          </div>
          <div v-else>
            <div style="padding-top:2px">
              <el-select
                size="mini"
                :popper-append-to-body="false"
                v-model="sltSeci"
                style="width:110px"
                placeholder="请选择"
              >
                <el-option
                  v-for="item in userSeciList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </div>
            <div style="margin-top:4px">
              <input
                class="btn"
                type="button"
                value="取消"
                @click="() => (showAddSeciInput = false)"
              />
              <input class="btn" type="button" value="确定" @click="saveSeci" />
            </div>
          </div>
        </div>
      </div>
      <div v-if="isEdit" class="input-row">
        <span>添加新基金:</span>
        <!-- <input v-model="fundcode" class="btn" type="text" placeholder="请输入基金代码" /> -->
        <el-select
          v-model="fundcode"
          multiple
          filterable
          :popper-append-to-body="false"
          remote
          size="mini"
          reserve-keyword
          @visible-change="selectChange"
          placeholder="请输入基金编码，支持按名称或编码搜索"
          :remote-method="remoteMethod"
          :loading="loading"
          style="width:300px"
        >
          <el-option
            v-for="item in searchOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <span style="float: left">{{ item.label }}</span>
            <span
              style="float: right; color: #8492a6; font-size: 13px;margim-right:20px;padding-right:15px"
              >{{ item.value }}</span
            >
          </el-option>
        </el-select>
        <input @click="save" class="btn" type="button" value="确定" />
      </div>
      <p v-if="isEdit" class="tips center">
        部分新发基金或QDII基金可以搜索到，但可能无法获取估值情况
      </p>
      <div
        v-if="isGetStorage"
        v-loading="loadingList"
        :element-loading-background="
          darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
        "
        class="table-row"
        style="min-height:160px"
      >
        <table :class="tableHeight">
          <thead>
            <tr>
              <th class="align-left">基金名称（{{ dataList.length }}）</th>
              <th v-if="isEdit">基金代码</th>
              <th v-if="showGSZ && !isEdit">估算净值</th>
              <th
                style="text-align:center"
                v-if="isEdit && (showCostRate || showCost)"
              >
                成本价
              </th>
              <th @click="sortList('amount')" v-if="showAmount" class="pointer">
                持有额
                <span :class="sortType.amount" class="down-arrow"></span>
              </th>
              <th
                @click="sortList('costGains')"
                v-if="showCost"
                class="pointer"
              >
                持有收益
                <span :class="sortType.costGains" class="down-arrow"></span>
              </th>
              <th
                @click="sortList('costGainsRate')"
                v-if="showCostRate"
                class="pointer"
              >
                持有收益率
                <span :class="sortType.costGainsRate" class="down-arrow"></span>
              </th>
              <th @click="sortList('gszzl')" class="pointer">
                涨跌幅
                <span :class="sortType.gszzl" class="down-arrow"></span>
              </th>
              <th @click="sortList('gains')" v-if="showGains" class="pointer">
                估算收益
                <span :class="sortType.gains" class="down-arrow"></span>
              </th>
              <th v-if="!isEdit">更新时间</th>
              <th
                style="text-align:center"
                v-if="
                  isEdit &&
                    (showAmount || showGains || showCost || showCostRate)
                "
              >
                持有份额
              </th>
              <th v-if="isEdit && BadgeContent == 1">特别关注</th>
              <th v-if="isEdit">删除</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(el, index) in dataList"
              :key="el.fundcode"
              :draggable="isEdit"
              :class="drag"
              @dragstart="handleDragStart($event, el)"
              @dragover.prevent="handleDragOver($event, el)"
              @dragenter="handleDragEnter($event, el, index)"
              @dragend="handleDragEnd($event, el)"
            >
              <td
                :class="
                  isEdit ? 'fundName-noclick align-left' : 'fundName align-left'
                "
                :title="el.name"
                @click.stop="!isEdit && fundDetail(el)"
              >
                <span class="hasReplace-tip" v-if="el.hasReplace">✔</span>{{ el.name }}
              </td>
              <td v-if="isEdit">{{ el.fundcode }}</td>
              <td v-if="showGSZ && !isEdit">{{ el.gsz }}</td>
              <td v-if="isEdit && (showCostRate || showCost)">
                <input
                  class="btn num"
                  placeholder="持仓成本价"
                  v-model="el.cost"
                  @input="changeCost(el, index)"
                  type="text"
                />
              </td>

              <td v-if="showAmount">
                {{
                  parseFloat(el.amount).toLocaleString("zh", {
                    minimumFractionDigits: 2,
                  })
                }}
              </td>
              <td v-if="showCost" :class="el.costGains >= 0 ? 'up' : 'down'">
                {{
                  parseFloat(el.costGains).toLocaleString("zh", {
                    minimumFractionDigits: 2,
                  })
                }}
              </td>
              <td
                v-if="showCostRate"
                :class="el.costGainsRate >= 0 ? 'up' : 'down'"
              >
                {{ el.cost > 0 ? el.costGainsRate + "%" : "" }}
              </td>
              <td :class="el.gszzl >= 0 ? 'up' : 'down'">{{ el.gszzl }}%</td>
              <td v-if="showGains" :class="el.gains >= 0 ? 'up' : 'down'">
                {{
                  parseFloat(el.gains).toLocaleString("zh", {
                    minimumFractionDigits: 2,
                  })
                }}
              </td>
              <td v-if="!isEdit">
                {{
                  el.hasReplace ? el.gztime.substr(5, 5) : el.gztime.substr(10)
                }}
                
              </td>
              <th
                style="text-align:center"
                v-if="
                  isEdit &&
                    (showAmount || showGains || showCost || showCostRate)
                "
              >
                <input
                  class="btn num"
                  placeholder="输入持有份额"
                  v-model="el.num"
                  @input="changeNum(el, index)"
                  type="text"
                />
              </th>
              <td v-if="isEdit && BadgeContent == 1">
                <input
                  @click="slt(el.fundcode)"
                  :class="el.fundcode == RealtimeFundcode ? 'slt' : ''"
                  class="btn edit"
                  value="✔"
                  type="button"
                />
              </td>
              <td v-if="isEdit">
                <input
                  @click="dlt(el.fundcode)"
                  class="btn red edit"
                  value="✖"
                  type="button"
                />
              </td>
            </tr>
          </tbody>
        </table>

        <!-- <table :class="tableHeight" class="detailTable">
          <thead>
            <tr>
              <th class="align-left">
                <div>基金名称</div>
                <p>基金编码</p>
              </th>
              <th>
                <div>持有收益率</div>
                <p>持有收益</p>
              </th>
              <th>
                <div>估算涨幅</div>
                <p>估算收益</p>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(el, index) in dataList"
              :key="el.fundcode"
              :draggable="isEdit"
              :class="drag"
              @dragstart="handleDragStart($event, el)"
              @dragover.prevent="handleDragOver($event, el)"
              @dragenter="handleDragEnter($event, el, index)"
              @dragend="handleDragEnd($event, el)"
            >
              <td
                :class="
                  isEdit ? 'fundName-noclick align-left' : 'fundName align-left'
                "
                :title="el.name"
                @click.stop="!isEdit && fundDetail(el)"
              >
                <div>{{ el.name }}</div>
                <p>{{ el.fundcode }}</p>
              </td>
              <td :class="el.costGains >= 0 ? 'up' : 'down'">
                <div>{{ el.cost > 0 ? el.costGainsRate + "%" : "" }}</div>
                <p>
                  {{
                  parseFloat(el.costGains).toLocaleString("zh", {
                    minimumFractionDigits: 2,
                  })
                }}
                </p>
              </td>
              <td :class="el.gszzl >= 0 ? 'up' : 'down'">
                <div>{{ el.gszzl }}%</div>
                <p>
                  {{
                    parseFloat(el.gains).toLocaleString("zh", {
                      minimumFractionDigits: 2,
                    })
                  }}
                </p>
              </td>
            </tr>
          </tbody>
        </table> -->
      </div>
    </div>
    <p v-if="isEdit" class="tips">
      特别关注功能介绍：指定一个基金，在程序图标中以角标的形式实时更新，请在设置中选择角标类型与内容。
    </p>

    <div v-show="isEdit" class="input-row gear-input-row">
      <el-switch
        v-model="darkMode"
        @change="changeDarkMode"
        active-color="#484848"
        inactive-color="#13ce66"
        inactive-text="标准模式"
        active-text="暗色模式"
      >
      </el-switch>
      <span class="slider-title">界面灰度：</span>
      <el-slider
        class="slider"
        v-model="grayscaleValue"
        @change="changeGrayscaleValue"
        :format-tooltip="formatTooltip"
      ></el-slider>
      <span class="slider-title">透明度：</span>
      <el-slider
        class="slider"
        :max="90"
        v-model="opacityValue"
        @change="changeOpacityValue"
        :format-tooltip="formatTooltip"
      ></el-slider>
      <!-- <input v-model="containerWidth" type="number" />
      <input v-model="containerHeight" type="number" /> -->
    </div>

    <div class="input-row">
      <input class="btn" type="button" @click="market" value="行情中心" />
      <input
        class="btn"
        v-if="isDuringDate"
        type="button"
        :value="isLiveUpdate ? '暂停更新' : '实时更新'"
        :title="
          isLiveUpdate ? '正在实时更新，点击暂停' : '已暂停，点击切换为实时更新'
        "
        @click="changeLiveUpdate"
      />
      <input class="btn" v-if="!isDuringDate" type="button" value="休市中" />
      <input
        class="btn"
        type="button"
        :value="isEdit ? '完成编辑' : '编辑'"
        @click="isEdit = !isEdit"
      />
      <input class="btn" type="button" value="设置" @click="option" />
      <input class="btn" type="button" value="日志" @click="changelog" />
      <input
        class="btn primary"
        type="button"
        title="φ(>ω<*)"
        value="打赏"
        @click="reward"
      />
    </div>
    <div class="input-row" v-if="showCost || showGains">
      <input
        v-if="showGains"
        class="btn"
        :class="allGains[0] >= 0 ? 'btn-up' : 'btn-down'"
        type="button"
        :title="
          allGains[0] >= 0 ? 'd=====(￣▽￣*)b 赞一个' : '∑(っ°Д°;)っ 大事不好啦'
        "
        :value="
          '日收益：' +
            parseFloat(allGains[0]).toLocaleString('zh', {
              minimumFractionDigits: 2,
            }) +
            (isNaN(allGains[1]) ? '' : '（' + allGains[1] + '%）')
        "
      />
      <input
        v-if="showCost"
        class="btn"
        :class="allCostGains[0] >= 0 ? 'btn-up' : 'btn-down'"
        type="button"
        :title="
          allCostGains[0] >= 0
            ? 'd=====(￣▽￣*)b 赞一个'
            : '∑(っ°Д°;)っ 大事不好啦'
        "
        :value="
          '持有收益：' +
            parseFloat(allCostGains[0]).toLocaleString('zh', {
              minimumFractionDigits: 2,
            }) +
            (isNaN(allCostGains[1]) ? '' : '（' + allCostGains[1] + '%）')
        "
      />
    </div>
    <div
      class="refresh"
      :class="{ isRefresh: isRefresh }"
      title="手动刷新数据"
      @click="refresh"
    >
      <i class="el-icon-refresh"></i>
    </div>
    <market
      :darkMode="darkMode"
      @close="closeCharts"
      ref="marketShadow"
    ></market>
    <ind-detail @close="closeCharts" :darkMode="darkMode" ref="indDetail">
    </ind-detail>
    <fund-detail
      @close="closeCharts"
      :fund="sltFund"
      :darkMode="darkMode"
      ref="fundDetail"
    ></fund-detail>
    <reward @close="rewardShadow = false" ref="reward"></reward>
    <change-log
      @close="closeChangelog"
      :darkMode="darkMode"
      ref="changelog"
      :top="30"
    ></change-log>
  </div>
</template>

<script>
const { version } = require("../../package.json");
import reward from "../common/reward";
import indDetail from "../common/indDetail";
import fundDetail from "../common/fundDetail";
import changeLog from "../common/changeLog";
import market from "../common/market";
//防抖
let timeout = null;
function debounce(fn, wait = 700) {
  if (timeout !== null) clearTimeout(timeout);
  timeout = setTimeout(fn, wait);
}

export default {
  components: {
    reward,
    fundDetail,
    indDetail,
    changeLog,
    market,
  },
  data() {
    return {
      isEdit: false,
      fundcode: "",
      isAdd: false,
      indFundData: [],
      isLiveUpdate: false,
      isDuringDate: false,
      RealtimeFundcode: null,
      RealtimeIndcode: null,
      dataList: [],
      dataListDft: [],
      myVar: null,
      myVar1: null,
      rewardShadow: false,
      checked: "wepay",
      showGains: false,
      showAmount: false,
      showCost: false,
      showCostRate: false,
      showGSZ: false,
      fundList: ["001618"],
      fundListM: [],
      sortType: {
        gszzl: "none",
        amount: "none",
        gains: "none",
        costGains: "none",
        costGainsRate: "none",
      },
      sortTypeObj: {
        name: null,
        value: null,
      },
      searchOptions: [],
      value: [],
      list: [],
      loading: false,
      dragging: null,
      showAddSeciInput: false,
      seciList: ["1.000001", "1.000300", "0.399001", "0.399006"],
      allSeciList: [
        {
          value: "1.000001",
          label: "上证指数",
        },
        {
          value: "1.000300",
          label: "沪深300",
        },
        {
          value: "0.399001",
          label: "深证成指",
        },
        {
          value: "1.000688",
          label: "科创50",
        },
        {
          value: "0.399006",
          label: "创业板指",
        },
        {
          value: "0.399005",
          label: "中小板指",
        },
        {
          value: "100.HSI",
          label: "恒生指数",
        },
        {
          value: "100.DJIA",
          label: "道琼斯",
        },
        {
          value: "100.NDX",
          label: "纳斯达克",
        },
        {
          value: "100.SPX",
          label: "标普500",
        },
      ],
      sltSeci: "",
      darkMode: false,
      normalFontSize: false,
      diyContainer: false,
      containerWidth: 790,
      containerHeight: 590,
      detailShadow: false,
      changelogShadow: false,
      sltFund: {},
      sltIndCode: "",
      localVersion: version,
      BadgeContent: 1,
      showBadge: 1,
      userId: null,
      loadingInd: false,
      loadingList: true,
      isGetStorage: false,
      zoom: {
        zoom: 1,
      },
      grayscale: {},
      grayscaleValue: 0,
      opacity: {},
      opacityValue: 0,
      isRefresh: false,
      marketShadow: false,
    };
  },
  mounted() {
    setTimeout(() => {
      let aa = window.screen.width;
      let bb = this.$refs.app.clientWidth;
      if (aa < bb) {
        this.zoom = {
          zoom: aa / bb,
        };
      }
    }, 10);
    this.init();
  },
  computed: {
    allGains() {
      let allGains = 0;
      let allNum = 0;
      this.dataList.forEach((val) => {
        allGains += parseFloat(val.gains);
        allNum += parseFloat(val.amount);
      });
      allGains = allGains.toFixed(2);
      let allGainsRate = ((allGains * 100) / allNum).toFixed(2);
      return [allGains, allGainsRate];
    },
    allCostGains() {
      let allCostGains = 0;
      let allNum = 0;
      this.dataList.forEach((val) => {
        allCostGains += parseFloat(val.costGains);
        allNum += parseFloat(val.amount);
      });
      allCostGains = allCostGains.toFixed(2);
      let allCostGainsRate = (
        (allCostGains * 100) /
        (allNum - allCostGains)
      ).toFixed(2);
      return [allCostGains, allCostGainsRate];
    },
    containerClass() {
      let className = "";
      if (this.normalFontSize) {
        className += "normalFontSize ";
      }
      if (this.darkMode) {
        className += "darkMode ";
      }
      if (this.changelogShadow) {
        className += "changelog-container";
      } else if (this.rewardShadow) {
        className += "more-height";
      } else if (this.detailShadow) {
        className += "detail-container";
      } else if (this.isEdit) {
        className += "more-width";
      } else {
        let tablist = [
          this.showAmount,
          this.showGains,
          this.showCost,
          this.showCostRate,
          this.showGSZ,
        ];
        let num = 0;
        tablist.forEach((val) => {
          if (val) {
            num++;
          }
        });
        className += "num-width-" + num;
      }
      return className;
    },
    userSeciList() {
      return this.allSeciList.filter((val) => {
        return this.seciList.indexOf(val.value) == -1;
      });
    },
    tableHeight() {
      if (this.isEdit) {
        return "table-more-height";
      }
    },
    drag() {
      if (this.isEdit) {
        return "table-drag";
      } else {
        return "";
      }
    },
  },
  watch: {
    //编辑状态停止更新
    isEdit(val) {
      if (val) {
        clearInterval(this.myVar);
        clearInterval(this.myVar1);
        this.dataList = [...this.dataListDft];
        for (const key in this.sortType) {
          if (this.sortType.hasOwnProperty(key)) {
            this.sortType[key] = "none";
          }
        }
      } else {
        this.checkInterval();
      }
    },
  },
  methods: {
    refresh() {
      this.init();
      this.isRefresh = true;
      setTimeout(() => {
        this.isRefresh = false;
      }, 1500);
    },
    formatTooltip(val) {
      return val + "%";
    },
    changeGrayscaleValue(val) {
      this.grayscale = {
        filter: "grayscale(" + val / 100 + ")",
      };
      chrome.storage.sync.set({
        grayscaleValue: this.grayscaleValue,
      });
    },
    changeOpacityValue(val) {
      this.opacity = {
        opacity: 1 - val / 100,
      };
      chrome.storage.sync.set({
        opacityValue: this.opacityValue,
      });
    },
    init() {
      chrome.storage.sync.get(
        [
          "RealtimeFundcode",
          "RealtimeIndcode",
          "fundListM",
          "showAmount",
          "showGains",
          "fundList",
          "seciList",
          "darkMode",
          "normalFontSize",
          "isLiveUpdate",
          "showCost",
          "showCostRate",
          "showGSZ",
          "version",
          "showBadge",
          "BadgeContent",
          "userId",
          "grayscaleValue",
          "opacityValue",
          "sortTypeObj",
        ],
        (res) => {
          this.fundList = res.fundList ? res.fundList : this.fundList;
          if (res.fundListM) {
            this.fundListM = res.fundListM;
          } else {
            for (const fund of this.fundList) {
              let val = {
                code: fund,
                num: 0,
              };
              this.fundListM.push(val);
            }
            chrome.storage.sync.set({
              fundListM: this.fundListM,
            });
          }
          if (res.userId) {
            this.userId = res.userId;
          } else {
            this.userId = this.getGuid();
            chrome.storage.sync.set({
              userId: this.userId,
            });
          }
          this.darkMode = res.darkMode ? res.darkMode : false;
          this.normalFontSize = res.normalFontSize ? res.normalFontSize : false;
          this.seciList = res.seciList ? res.seciList : this.seciList;
          this.showAmount = res.showAmount ? res.showAmount : false;
          this.showGains = res.showGains ? res.showGains : false;
          this.RealtimeFundcode = res.RealtimeFundcode;
          this.RealtimeIndcode = res.RealtimeIndcode;
          this.isLiveUpdate = res.isLiveUpdate ? res.isLiveUpdate : false;
          this.showCost = res.showCost ? res.showCost : false;
          this.showCostRate = res.showCostRate ? res.showCostRate : false;
          this.showGSZ = res.showGSZ ? res.showGSZ : false;
          this.BadgeContent = res.BadgeContent ? res.BadgeContent : 1;
          this.showBadge = res.showBadge ? res.showBadge : 1;
          this.grayscaleValue = res.grayscaleValue ? res.grayscaleValue : 0;
          this.opacityValue = res.opacityValue ? res.opacityValue : 0;
          this.sortTypeObj = res.sortTypeObj ? res.sortTypeObj : {};

          if (this.seciList.length > 0) {
            this.loadingInd = true;
          }

          this.grayscale = {
            filter: "grayscale(" + this.grayscaleValue / 100 + ")",
          };
          this.opacity = {
            opacity: 1 - this.opacityValue / 100,
          };

          this.isGetStorage = true;
          this.getIndFundData();
          this.getData();
          this.checkInterval(true);

          let ver = res.version ? res.version : "1.0.0";
          if (ver != this.localVersion) {
            this.changelog();
          }
        }
      );
    },
    getGuid() {
      return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(
        c
      ) {
        var r = (Math.random() * 16) | 0,
          v = c == "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
    },
    indDetail(val) {
      // this.sltIndCode = val.f13 + "." + val.f12;
      this.detailShadow = true;
      this.$refs.indDetail.init(val);
    },
    fundDetail(val) {
      this.sltFund = val;
      this.detailShadow = true;
      this.$refs.fundDetail.init();
    },
    closeCharts() {
      this.detailShadow = false;
    },
    market() {
      this.detailShadow = true;
      this.$refs.marketShadow.init();
    },
    checkInterval(isFirst) {
      clearInterval(this.myVar);
      clearInterval(this.myVar1);
      chrome.runtime.sendMessage({ type: "DuringDate" }, (response) => {
        this.isDuringDate = response.farewell;
        if (this.isLiveUpdate && this.isDuringDate) {
          if (!isFirst) {
            this.getIndFundData();
            this.getData();
          }
          this.myVar = setInterval(() => {
            this.getIndFundData();
          }, 5 * 1000);
          this.myVar1 = setInterval(() => {
            this.getData();
          }, 60 * 1000);
        } else {
          clearInterval(this.myVar);
          clearInterval(this.myVar1);
        }
      });
    },
    selectChange() {
      this.searchOptions = [];
    },
    remoteMethod(query) {
      if (query !== "") {
        this.loading = true;
        let url =
          "https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?&m=9&key=" +
          query +
          "&_=" +
          new Date().getTime();
        this.$axios.get(url).then((res) => {
          this.searchOptions = res.data.Datas.filter((val) => {
            let hasCode = this.fundListM.some((currentValue, index, array) => {
              return currentValue.code == val.CODE;
            });
            return !hasCode;
          }).map((val) => {
            return {
              value: val.CODE,
              label: val.NAME,
            };
          });
          this.loading = false;
        });
      } else {
        this.searchOptions = [];
      }
    },

    option() {
      chrome.tabs.create({ url: "/options/options.html" });
    },
    reward() {
      this.rewardShadow = true;
      this.$refs.reward.init();
    },
    changelog() {
      this.changelogShadow = true;
      this.$refs.changelog.init();
    },
    closeChangelog() {
      this.changelogShadow = false;
      chrome.storage.sync.set({
        version: this.localVersion,
      });
    },
    sortList(type) {
      for (const key in this.sortType) {
        if (this.sortType.hasOwnProperty(key)) {
          if (key != type) {
            this.sortType[key] = "none";
          }
        }
      }
      this.sortType[type] =
        this.sortType[type] == "desc"
          ? "asc"
          : this.sortType[type] == "asc"
          ? "none"
          : "desc";
      if (this.sortType[type] == "none") {
        this.dataList = [...this.dataListDft];
      } else {
        this.dataList = this.dataList.sort(
          this.compare(type, this.sortType[type])
        );
      }
      this.sortTypeObj = {
        name: type,
        type: this.sortType[type],
      };
      chrome.storage.sync.set({
        sortTypeObj: this.sortTypeObj,
      });
    },
    compare(property, type) {
      return function(obj1, obj2) {
        var val1 = obj1[property];
        var val2 = obj2[property];
        if (type == "asc") {
          return val1 - val2;
        } else {
          return val2 - val1;
        }
      };
    },

    changeDarkMode() {
      chrome.storage.sync.set({
        darkMode: this.darkMode,
      });
    },
    changeLiveUpdate() {
      chrome.storage.sync.set(
        {
          isLiveUpdate: !this.isLiveUpdate,
        },
        () => {
          this.isLiveUpdate = !this.isLiveUpdate;
          this.checkInterval();
        }
      );
    },
    saveSeci() {
      this.seciList.push(this.sltSeci);
      chrome.storage.sync.set(
        {
          seciList: this.seciList,
        },
        () => {
          this.sltSeci = "";
          this.getIndFundData();
        }
      );
    },
    dltIndFund(ind) {
      this.seciList.splice(ind, 1);
      chrome.storage.sync.set(
        {
          seciList: this.seciList,
        },
        () => {
          this.getIndFundData();
        }
      );
    },
    getIndFundData() {
      let seciListStr = this.seciList.join(",");
      let url =
        "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f2,f3,f4,f12,f13,f14&secids=" +
        seciListStr +
        "&_=" +
        new Date().getTime();
      this.$axios.get(url).then((res) => {
        this.loadingInd = false;
        this.indFundData = res.data.data.diff;
      });
    },
    getData(type) {
      let fundlist = this.fundListM.map((val) => val.code).join(",");
      let url =
        "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo?pageIndex=1&pageSize=200&plat=Android&appType=ttjj&product=EFund&Version=1&deviceid=" +
        this.userId +
        "&Fcodes=" +
        fundlist;
      this.$axios
        .get(url)
        .then((res) => {
          this.loadingList = false;
          let data = res.data.Datas;
          this.dataList = [];
          let dataList = [];

          data.forEach((val) => {
            let data = {
              fundcode: val.FCODE,
              name: val.SHORTNAME,
              jzrq: val.PDATE,
              dwjz: isNaN(val.NAV) ? null : val.NAV,
              gsz: isNaN(val.GSZ) ? null : val.GSZ,
              gszzl: isNaN(val.GSZZL) ? 0 : val.GSZZL,
              gztime: val.GZTIME,
            };
            if (val.PDATE != "--" && val.PDATE == val.GZTIME.substr(0, 10)) {
              data.gsz = val.NAV;
              data.gszzl = isNaN(val.NAVCHGRT) ? 0 : val.NAVCHGRT;
              data.hasReplace = true;
            }

            let slt = this.fundListM.filter(
              (item) => item.code == data.fundcode
            );
            data.num = slt[0].num;
            data.cost = slt[0].cost;
            data.amount = this.calculateMoney(data);
            data.gains = this.calculate(data, data.hasReplace);
            data.costGains = this.calculateCost(data);
            data.costGainsRate = this.calculateCostRate(data);

            if (data.fundcode == this.RealtimeFundcode) {
              if (this.showBadge == 1) {
                if (this.BadgeContent == 1) {
                  chrome.runtime.sendMessage({
                    type: "refreshBadge",
                    data: data,
                  });
                }
              }
            }

            dataList.push(data);
          });
          if (this.showBadge == 1) {
            if (this.BadgeContent == 2) {
              chrome.runtime.sendMessage({
                type: "refreshBadgeAllGains",
                data: data,
              });
            }
          }

          this.dataListDft = [...dataList];
          if (type == "add") {
            this.dataList = dataList;
          } else if (this.sortTypeObj.type != "none") {
            this.sortType[this.sortTypeObj.name] = this.sortTypeObj.type;
            this.dataList = dataList.sort(
              this.compare(this.sortTypeObj.name, this.sortTypeObj.type)
            );
          } else {
            this.dataList = dataList;
          }
        })
        .catch((error) => {});
    },
    changeNum(item, ind) {
      debounce(() => {
        for (let fund of this.fundListM) {
          if (fund.code == item.fundcode) {
            fund.num = item.num;
          }
        }
        chrome.storage.sync.set(
          {
            fundListM: this.fundListM,
          },
          () => {
            item.amount = this.calculateMoney(item);
            item.gains = this.calculate(item, item.hasReplace);
            item.costGains = this.calculateCost(item);
            chrome.runtime.sendMessage({ type: "refresh" });
          }
        );
      });
    },
    changeCost(item, ind) {
      debounce(() => {
        for (let fund of this.fundListM) {
          if (fund.code == item.fundcode) {
            fund.cost = item.cost;
          }
        }
        chrome.storage.sync.set(
          {
            fundListM: this.fundListM,
          },
          () => {
            item.costGains = this.calculateCost(item);
            item.costGainsRate = this.calculateCostRate(item);
          }
        );
      });
    },
    calculateMoney(val) {
      let sum = (val.dwjz * val.num).toFixed(2);
      return sum;
    },
    calculate(val, hasReplace) {
      var sum = 0;
      let num = val.num ? val.num : 0;
      if (hasReplace) {
        sum = ((val.dwjz - val.dwjz / (1 + val.gszzl * 0.01)) * num).toFixed(2);
      } else {
        if (val.gsz) {
          sum = ((val.gsz - val.dwjz) * num).toFixed(2);
        }
      }
      return sum;
    },
    calculateCost(val) {
      if (val.cost) {
        let sum = ((val.dwjz - val.cost) * val.num).toFixed(2);
        return sum;
      } else {
        return 0;
      }
    },
    calculateCostRate(val) {
      if (val.cost && val.cost != 0) {
        let sum = (((val.dwjz - val.cost) / val.cost) * 100).toFixed(2);
        return sum;
      } else {
        return 0;
      }
    },
    save() {
      this.fundcode.forEach((code) => {
        let val = {
          code: code,
          num: 0,
        };
        this.fundListM.push(val);
      });

      chrome.storage.sync.set(
        {
          fundListM: this.fundListM,
        },
        () => {
          this.fundcode = [];
          this.getData("add");
          chrome.runtime.sendMessage({ type: "refresh" });
        }
      );
    },
    sltInd(val) {
      let code = val.f13 + "." + val.f12;
      if (code == this.RealtimeIndcode) {
        chrome.storage.sync.set(
          {
            RealtimeIndcode: null,
          },
          () => {
            this.RealtimeIndcode = null;
            chrome.runtime.sendMessage({ type: "endInterval" });
          }
        );
      } else {
        chrome.storage.sync.set(
          {
            RealtimeIndcode: code,
          },
          () => {
            this.RealtimeIndcode = code;
            chrome.runtime.sendMessage({ type: "refresh" });
          }
        );
      }
    },
    slt(id) {
      if (id == this.RealtimeFundcode) {
        chrome.storage.sync.set(
          {
            RealtimeFundcode: null,
          },
          () => {
            this.RealtimeFundcode = null;
            chrome.runtime.sendMessage({ type: "endInterval" });
          }
        );
      } else {
        chrome.storage.sync.set(
          {
            RealtimeFundcode: id,
          },
          () => {
            this.RealtimeFundcode = id;
            chrome.runtime.sendMessage({ type: "refresh" });
          }
        );
      }
    },
    dlt(id) {
      this.fundListM = this.fundListM.filter(function(ele) {
        return ele.code != id;
      });

      if (id == this.RealtimeFundcode) {
        chrome.storage.sync.set(
          {
            RealtimeFundcode: null,
          },
          () => {
            this.RealtimeFundcode = null;
            if (this.BadgeContent == 1) {
              chrome.runtime.sendMessage({ type: "endInterval" });
            }
          }
        );
      }
      chrome.storage.sync.set(
        {
          fundListM: this.fundListM,
        },
        () => {
          this.dataList = this.dataList.filter(function(ele) {
            return ele.fundcode != id;
          });
          if (this.BadgeContent == 2) {
            chrome.runtime.sendMessage({ type: "refresh" });
          }
        }
      );
    },
    handleDragStart(e, item) {
      this.dragging = item;
    },
    handleDragOver(e) {
      e.dataTransfer.dropEffect = "move";
    },
    handleDragEnd(e, item) {
      this.dragging = null;
      if (item.fundcode) {
        chrome.storage.sync.set(
          {
            fundListM: this.fundListM,
          },
          () => {}
        );
      } else if (item.f12) {
        chrome.storage.sync.set(
          {
            seciList: this.seciList,
          },
          () => {}
        );
      }
    },
    handleDragEnter(e, item, index) {
      // 基金排序
      if (this.dragging && this.dragging.fundcode && item.fundcode) {
        e.dataTransfer.effectAllowed = "move";
        if (item.fundcode === this.dragging.fundcode) {
          return;
        }
        const newItems = [...this.fundListM];
        const src = newItems.findIndex((n) => n.code == this.dragging.fundcode);
        const dst = newItems.findIndex((n) => n.code == item.fundcode);
        // // 替换
        newItems.splice(dst, 0, ...newItems.splice(src, 1));

        this.fundListM = newItems;

        //数据列表也同步更新
        const newDataItems = [...this.dataList];
        const dataSrc = newDataItems.findIndex(
          (n) => n.fundcode == this.dragging.fundcode
        );
        const dataDst = newDataItems.findIndex(
          (n) => n.fundcode == item.fundcode
        );
        newDataItems.splice(dataDst, 0, ...newDataItems.splice(dataSrc, 1));
        this.dataList = newDataItems;
      } else if (this.dragging && this.dragging.f12 && item.f12) {
        e.dataTransfer.effectAllowed = "move";
        if (item.f12 === this.dragging.f12) {
          return;
        }
        const newIndItems = [...this.seciList];
        const indSrc = newIndItems.findIndex(
          (n) => n.split(".")[1] == this.dragging.f12
        );
        const indDst = newIndItems.findIndex(
          (n) => n.split(".")[1] == item.f12
        );
        newIndItems.splice(indDst, 0, ...newIndItems.splice(indSrc, 1));
        this.seciList = newIndItems;

        const newIndDataItems = [...this.indFundData];
        const indDataSrc = newIndDataItems.findIndex(
          (n) => n.f12 == this.dragging.f12
        );
        const indDataDst = newIndDataItems.findIndex((n) => n.f12 == item.f12);
        newIndDataItems.splice(
          indDataDst,
          0,
          ...newIndDataItems.splice(indDataSrc, 1)
        );
        this.indFundData = newIndDataItems;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  min-width: 400px;
  min-height: 150px;
  overflow-y: auto;
  padding: 10px 7px;
  box-sizing: border-box;
  position: relative;
  font-size: 12px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.refresh {
  position: absolute;
  right: 10px;
  width: 18px;
  bottom: 12px;

  cursor: pointer;
  i {
    color: #409eff;
    font-size: 18px;
    font-weight: bold;
  }
}

.refresh.isRefresh {
  animation: changDeg 1.5s linear 0s infinite;
}

@keyframes changDeg {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}

.more-height {
  min-height: 450px;
}

.more-width {
  min-width: 785px;
}

.changelog-container {
  min-height: 575px;
  min-width: 550px;
}

.table-more-height {
  min-height: 160px;
}
.table-drag {
  cursor: move;
}

.container {
  &.num-width-1 {
    min-width: 420px;
  }
  &.num-width-2 {
    min-width: 480px;
  }
  &.num-width-3 {
    min-width: 540px;
  }
  &.num-width-4 {
    min-width: 610px;
  }
  &.num-width-5 {
    min-width: 680px;
  }
}

.table-row {
  max-height: 425px;
  overflow-y: auto;
}

.hasReplace {
  background-color: #409eff;
}

.hasReplace-tip {
  display: inline-block;
  padding: 0 2px;
  margin-right: 2px;
  border-radius: 2px;
  line-height: 12px;
  color: #409eff;
  border: 1px solid #409eff;
}

table {
  margin: 0 auto;
  width: 100%;
  border-collapse: collapse;
  text-align: right;
}
.align-left {
  text-align: left;
}

.center {
  text-align: center;
}

table th {
  padding: 8px 6px;
}

table td {
  padding: 6px 6px 5px;
}

.up {
  color: #f56c6c;
  font-weight: bold;
}

.down {
  color: #4eb61b;
  font-weight: bold;
}

tbody tr:hover {
  background: #f5fafe;
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
  margin: 0 3px;
  outline: none;
  border: 1px solid #dcdfe6;
}

.btn.edit {
  padding: 2px 5px;
  margin: 0;
}

.btn.red {
  color: #f56c6c;
}

.btn.num {
  width: 75px;
  padding: 3px 6px;
}

.btn-up {
  color: #f56c6c;
  border-color: #f56c6c;
  font-weight: bold;
}

.btn-down {
  color: #4eb61b;
  border-color: #4eb61b;
  font-weight: bold;
}

.slt {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}

.input-row {
  text-align: center;
  margin-top: 10px;
}
.gear-input-row {
  display: flex;
  justify-content: center;
  align-items: center;
  .slider-title {
    font-size: 14px;
    margin: 0 5px 0 15px;
  }
  .slider {
    display: inline-block;
    width: 20%;
  }
}

.tab-col {
  flex: 1;
  margin: 0 4px;
  text-align: center;
  h5 {
    margin: 4px 0;
    font-size: 12px;
    .dltBtn {
      margin-left: 3px;
    }
  }
  p {
    margin: 4px 0;
  }
  .addSeci {
    margin: 10px auto;
    width: 40px;
    height: 40px;
    cursor: pointer;
    line-height: 40px;
    border: 1px solid #dcdfe6;
    border-radius: 50%;
  }
}
.indFund {
  cursor: pointer;
}

.tab-row:after,
.tab-row:before {
  display: table;
  content: "";
}

.tab-row:after {
  clear: both;
}

.tab-row {
  padding: 6px 0;
  display: flex;
  margin: 0 -3px;
}

.primary {
  color: #409eff;
  border-color: #409eff;
}

.tips {
  font-size: 12px;
  margin: 0;
  color: #aaaaaa;
  line-height: 1.4;
  padding: 5px 15px;
}

.fundName {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
}

.fundName-noclick {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fundName:hover {
  color: #409eff;
}

.down-arrow {
  display: inline-block;
  position: relative;
  width: 8px;
  height: 0;
}

.down-arrow::after {
  display: inline-block;
  content: " ";
  height: 6px;
  width: 6px;
  border-width: 0 1px 1px 0;
  border-color: #666;
  border-style: solid;
  transform-origin: center;
  transition: all 0.3s;
  position: absolute;
  right: 0;
}
.down-arrow.desc::after {
  transform-origin: center;
  transform: rotate(45deg);
  top: -10px;
}
.down-arrow.asc::after {
  transform-origin: center;
  transform: rotate(-135deg);
  top: -6px;
}

.down-arrow.none {
  display: none;
}

.pointer {
  cursor: pointer;
  user-select: none;
}

//标准字号
.normalFontSize {
  min-width: 450px;
  font-size: 14px;
  &.num-width-1 {
    min-width: 500px;
  }
  &.num-width-2 {
    min-width: 580px;
  }
  &.num-width-3 {
    min-width: 630px;
  }
  &.num-width-4 {
    min-width: 690px;
  }
  &.num-width-5 {
    min-width: 750px;
  }

  .btn,
  .tips {
    font-size: 14px;
  }
  .tab-col {
    h5 {
      font-size: 14px;
    }
  }
}

.detail-container {
  min-height: 450px;
  min-width: 610px;
}

.detailTable {
  th,
  td {
    p {
      margin: 2px 0;
      color: rgba($color: #000000, $alpha: 0.6);
    }
  }
}

//暗黑主题
.container.darkMode {
  color: rgba($color: #ffffff, $alpha: 0.6);
  background-color: #121212;
  .refresh {
    color: rgba($color: #409eff, $alpha: 0.6);
  }
  .btn {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.6);
  }
  .primary {
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
    background-color: rgba($color: #409eff, $alpha: 0.6);
  }
  /deep/ .el-input__inner {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
  }
  /deep/ .el-select__input {
    color: rgba($color: #ffffff, $alpha: 0.6);
  }

  /deep/ tbody tr:hover {
    background-color: rgba($color: #ffffff, $alpha: 0.12);
  }

  .slt {
    border: 1px solid rgba($color: #67c23a, $alpha: 0.6);
    background-color: rgba($color: #67c23a, $alpha: 0.6);
  }

  .btn.red {
    border: 1px solid rgba($color: #f56c6c, $alpha: 0.6);
    background-color: rgba($color: #f56c6c, $alpha: 0.6);
  }

  .btn-up {
    border: 1px solid rgba($color: #f56c6c, $alpha: 0.6);
    background-color: rgba($color: #f56c6c, $alpha: 0.6);
  }

  .btn-down {
    border: 1px solid rgba($color: #4eb61b, $alpha: 0.6);
    background-color: rgba($color: #4eb61b, $alpha: 0.6);
  }

  .tab-col {
    background-color: rgba($color: #ffffff, $alpha: 0.09);
    border-radius: 5px;
  }

  table {
    background-color: rgba($color: #ffffff, $alpha: 0.12);
    border-radius: 5px;
  }

  ::placeholder {
    color: rgba($color: #ffffff, $alpha: 0.38);
  }

  /deep/ .el-select .el-input.is-focus .el-input__inner {
    border-color: rgba($color: #409eff, $alpha: 0.6);
  }

  /deep/ .el-select .el-tag {
    background-color: rgba($color: #ffffff, $alpha: 0.14);
    color: rgba($color: #ffffff, $alpha: 0.6);
  }

  /deep/ .el-select-dropdown {
    background-color: #383838;
    border: 1px solid rgba($color: #ffffff, $alpha: 0.38);
    .popper__arrow::after {
      border-bottom-color: #383838;
    }
    .el-scrollbar {
      background-color: rgba($color: #ffffff, $alpha: 0.16);
    }
    .el-select-dropdown__item {
      color: rgba($color: #ffffff, $alpha: 0.6);
    }

    .el-select-dropdown__item.hover,
    .el-select-dropdown__item:hover {
      background-color: rgba($color: #ffffff, $alpha: 0.08);
    }
    .el-select-dropdown__item.selected {
      color: rgba($color: #409eff, $alpha: 0.6);
      background-color: rgba($color: #ffffff, $alpha: 0.08);
    }
    .el-select-dropdown__item.selected::after {
      color: rgba($color: #409eff, $alpha: 0.6);
    }
  }

  /deep/ .el-switch__label.is-active {
    color: rgba($color: #409eff, $alpha: 0.87);
  }
  /deep/ .el-switch__label {
    color: rgba($color: #ffffff, $alpha: 0.6);
  }

  /deep/ .hasReplace-tip {
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #409eff, $alpha: 0.6);
    background-color: rgba($color: #409eff, $alpha: 0.6);
  }
}
</style>
