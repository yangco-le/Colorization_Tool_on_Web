import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import axios from 'axios'

Vue.use(ElementUI);
Vue.prototype.$axios = axios
Vue.prototype.$url = 'http://127.0.0.1:8000/'

new Vue({
  el: '#app',
  render: h => h(App)
});