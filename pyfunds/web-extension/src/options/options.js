import Vue from "vue";
import App from "./App";
import axios from "axios";
import {
  Switch,
  Message,
  Radio,
  RadioGroup,
  Button,
  Input,
  Loading,
  Dialog
} from 'element-ui';

import VueClipboard from "vue-clipboard2";
Vue.use(VueClipboard)


Vue.use(Switch)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(Button)
Vue.use(Input)
Vue.use(Dialog)
Vue.use(Loading)

Vue.prototype.$axios = axios;
Vue.prototype.$message = Message;
Vue.prototype.$ELEMENT = { size: 'mini' };

Vue.use(Loading.directive);
Vue.prototype.$loading = Loading.service;

/* eslint-disable no-new */
new Vue({
  el: "#app",

  render: h => h(App)
});