// グローバルなStore
import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';
// module
import header from './header';


Vue.use(Vuex);

export default new Vuex.Store({
  strict: true,
  plugins: process.env.NODE_ENV !== 'production'
    ? [createLogger()]
    : [],
  modules: {
    header,
  },
  state: {
  },
  mutations: {
  },
});
