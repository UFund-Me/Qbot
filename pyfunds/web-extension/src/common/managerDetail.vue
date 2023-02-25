<template>
  <div v-if="boxShadow" class="shadow" :class="boxClass">
    <div class="manager-box">
      <div
        v-loading="loadingManager"
        :element-loading-background="
          darkMode ? 'rgba(0, 0, 0, 0.9)' : 'rgba(255, 255, 255, 0.9)'
        "
        class="manager-content"
        ref="manager"
      >
        <div>
          <h5>基金经理变动一览</h5>
          <div class="table-row">
            <table>
              <thead>
                <tr>
                  <th>起始期</th>
                  <th>截止期</th>
                  <th>基金经理</th>
                  <th>任职期</th>
                  <th>任职涨幅</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="el in managerList" :key="el.MGRID">
                  <td>{{ el.FEMPDATE }}</td>
                  <td>{{ el.LEMPDATE == "" ? "至今" : el.LEMPDATE }}</td>
                  <td>{{ el.MGRNAME }}</td>
                  <td>{{ el.DAYS.toFixed(0) }}天</td>
                  <td :class="el.PENAVGROWTH >= 0 ? 'up' : 'down'">
                    {{ el.PENAVGROWTH.toFixed(2) }}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <h5>现任基金经理简介</h5>
          <div v-for="el in managerDetail" :key="el.MGRID">
            <div class="manager-info">
              <div class="img-row">
                <img :src="el.PHOTOURL" :alt="el.MGRNAME" />
              </div>
              <div class="info-row">
                <p>姓名：{{ el.MGRNAME }}</p>
                <p>上任日期：{{ el.FEMPDATE }}</p>
                <p>管理年限：{{ el.DAYS }}</p>
              </div>
            </div>
            <div class="manager-resume">{{ el.RESUME }}</div>
          </div>
        </div>
      </div>

      <div class="tab-row">
        <input class="btn" type="button" value="返回列表" @click="close" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "managerDetail",
  props: {
    darkMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      boxShadow: false,
      loadingManager: false,
      managerList: [],
      managerDetail: [],
    };
  },
  watch: {},
  computed: {
    boxClass() {
      let className = "";
      if (this.darkMode) {
        className += "darkMode ";
      }
      return className;
    },
  },
  mounted() {},
  methods: {
    init(val) {
      this.boxShadow = true;
      this.getManagerList(val);
      this.getMangerDetail(val);
    },
    getManagerList(code) {
      let url = `https://fundmobapi.eastmoney.com/FundMApi/FundManagerList.ashx?FCODE=${code}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        this.managerList = res.data.Datas;
      });
    },
    getMangerDetail(code) {
      let url = `https://fundmobapi.eastmoney.com/FundMApi/FundMangerDetail.ashx?FCODE=${code}&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&_=${new Date().getTime()}`;
      this.$axios.get(url).then((res) => {
        this.managerDetail = res.data.Datas;
      });
    },

    close() {
      this.boxShadow = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.up {
  color: #f56c6c;
  font-weight: bold;
}

.down {
  color: #4eb61b;
  font-weight: bold;
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
  padding: 10px 20px 0;
  margin: 35px auto 0;
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
h5 {
  margin: 0;
  padding: 7px;
  font-size: 15px;
}
.table-row {
  padding: 5px 10px;
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
.manager-info {
  padding: 5px 10px 0;
  display: flex;
  text-align: left;
  .img-row {
    flex: 0 0 100px;
    img {
      width: 80px;
      height: auto;
    }
  }
  .info-row {
    flex: 1 1 auto;
    p {
      margin: 12px;
    }
  }
}
.manager-resume {
  text-align: justify;
  text-indent: 2em;
  padding: 5px 10px;
  line-height: 1.5;
  border-bottom: 1px solid #dddddd;
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
  .manager-resume {
    border-bottom: 1px solid rgba($color: #ffffff, $alpha: 0.38);
  }
}
.darkMode table tr:nth-child(even) {
  background-color: rgba($color: #ffffff, $alpha: 0.05);
}
.tab-row {
  padding: 12px 0;
}

.manager-content {
  width: 100%;
  height: 330px;
  overflow-y: auto;
}
</style>
