import Vue from 'vue';
import Router from 'vue-router';
import WebSocketMiddleware from './middlewares/websocket';

import DefaultLayout from '../components/layouts/DefaultLayout.vue';
import NotFound from '../pages/NotFound.vue';
import Home from '../pages/Home/Index.vue';
import Board from '../pages/Board/Index.vue';


Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: DefaultLayout,
      // localhost:3000へのアクセスでHome/Index.vueが表示
      children: [
        {
          path: '',
          component: Home,
        },
        {
          path: 'boards/:boardId',
          component: Board,
          // Vue-routerのルーティングの定義にmeta.wsをセットすれば
          // ルーティングの切替時にWebSocketへ接続が行われる
          meta: {
            ws: route => route.path,
          },
        },
      ]
    },
    {
      path: '*',
      component: NotFound,
    },
  ],
});

WebSocketMiddleware(router);
export default router;
