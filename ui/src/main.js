import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuex from 'vuex'
import 'carbon-components/css/carbon-components.css';
import CarbonComponentsVue from '@carbon/vue/src/index';
import store from './store'

Vue.use(CarbonComponentsVue);
Vue.use(Vuex);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
