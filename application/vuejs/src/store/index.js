// グローバルなStore
import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';
// module
import header from './_layouts/header';
import home from './pages/home';
import board from './pages/board';


Vue.use(Vuex);

// VueでWebSocketを使うには
// vue-native-websocketを使う
export default new Vuex.Store({
  strict: true,
  plugins: process.env.NODE_ENV !== 'production'
    ? [createLogger()]
    : [],
  modules: {
    header,
    home,
    board,
  },
  state: {
    socket: null,  // 接続中のsocketを保持する
  },
  mutations: {
    // 必要なmutationはSOCKET_ONOPEN とSOCKET_ONCLOSE
    // あとはデバッグ用
    SOCKET_ONOPEN(state, event) {
      console.log('SOCKET_ONOPEN', event);
      // 接続が確立されたWebSocketのセッションオブジェクトが
      // state.socketに入るので
      // 実際にメッセージをやり取りする時はstate.socketを通して行う
      // 接続時にStoreにwebsocketオブジェクトを登録する
      state.socket = event.target;
    },
    SOCKET_ONCLOSE(state, event) {
      console.log('SOCKET_ONCLOSE', event);
      // 接続終了にStoreにwebsocketオブジェクトを解除する
      state.socket = null;
    },
    SOCKET_ONERROR(state, event) {
      console.log('SOCKET_ONERROR', event);
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE(state, message) {
      console.log('SOCKET_ONMESSAGE', message);
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.log('SOCKET_RECONNECT', count);
    },
    SOCKET_RECONNECT_ERROR(state) {
      console.log('SOCKET_RECONNECT_ERROR', state);
    },
  },
});

