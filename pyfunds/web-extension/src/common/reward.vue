<template>
  <div v-if="rewardShadow" class="shadow">
    <div class="reward-box" :style="{ marginTop: top + 'px' }">
      <div class="tab-row">
        <button
          @click="checked = 'wepay'"
          :class="checked == 'wepay' ? 'checked' : ''"
        >
          微信
        </button>
        <button
          @click="checked = 'alipay'"
          :class="checked == 'alipay' ? 'checked' : ''"
        >
          支付宝
        </button>
      </div>
      <div class="qrcode">
        <img
          :src="
            checked == 'wepay'
              ? './../icons/qrcode/wepay.png'
              : './../icons/qrcode/alipay.png'
          "
        />
      </div>
      <p class="tips reward-tips">
        感谢有您的支持，Qbot自选基金才能一直保持更新，增加更多功能。
      </p>
      <div class="tab-row">
        <input
          class="btn success"
          type="button"
          value="打赏好了"
          @click="close"
        />
        <input class="btn" type="button" value="下次一定" @click="close" />
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    top: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      rewardShadow: false,
      checked: "wepay",
    };
  },
  mounted() {},
  methods: {
    init() {
      this.rewardShadow = true;
    },
    close() {
      this.rewardShadow = false;
      this.$emit("close", false);
    },
  },
};
</script>

<style lang="scss" scoped>
.shadow {
  position: fixed;
  width: 100%;
  height: 100%;
  padding: 20px 40px;
  z-index: 1001;
  box-sizing: border-box;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.7);
}

.reward-box {
  background: #ffffff;
  border-radius: 15px;
  width: 326px;
  margin: 0 auto;
  text-align: center;
  line-height: 1;
  vertical-align: middle;
  font-size: 0;
}

.reward-box button {
  line-height: 1;
  white-space: nowrap;
  vertical-align: middle;
  background: #fff;
  border: 1px solid #dcdfe6;
  font-weight: 500;
  border-left: 0;
  color: #606266;
  -webkit-appearance: none;
  text-align: center;
  box-sizing: border-box;
  margin: 0;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  padding: 12px 20px;
  font-size: 14px;
  width: 85px;
  position: relative;
  display: inline-block;
  outline: none;
}

.reward-box button:first-child {
  border-left: 1px solid #dcdfe6;
  border-radius: 4px 0 0 4px;
  box-shadow: none !important;
}

.reward-box button:last-child {
  border-radius: 0 4px 4px 0;
}

.reward-box button.checked {
  color: #fff;
  background-color: #409eff;
  border-color: #409eff;
}

.qrcode img {
  width: 256px;
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

.tips {
  font-size: 12px;
  margin: 0;
  color: #aaaaaa;
  line-height: 1.4;
  padding: 5px 15px;
}

.reward-tips {
  padding: 0 50px;
  margin-top: 5px;
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
.success {
  color: #4eb61b;
  border-color: #4eb61b;
}

.darkMode .reward-box {
  color: rgba($color: #ffffff, $alpha: 0.6);
  background-color: #373737;
  .btn {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.6);
  }
  .success {
    border: 1px solid rgba($color: #4eb61b, $alpha: 0.6);
    background-color: rgba($color: #4eb61b, $alpha: 0.6);
  }

  button {
    background-color: rgba($color: #ffffff, $alpha: 0.16);
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #ffffff, $alpha: 0.38);
  }

  button.checked {
    color: rgba($color: #ffffff, $alpha: 0.6);
    border: 1px solid rgba($color: #409eff, $alpha: 0.38);
    background-color: rgba($color: #409eff, $alpha: 0.6);
  }
}
</style>
