import Vue from 'vue';
import Router from 'vue-router';
import WebSocketMiddleware from './middlewares/websocket';

import DefaultLayout from '../pages/_layouts/DefaultLayout.vue';
import NotFound from '../pages/NotFound.vue';
import Home from '../pages/Home.vue';
import Board from '../pages/Board.vue';
import CardShow from '../pages/components/Board/Card/Show.vue';


Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: DefaultLayout,
      // localhost:3000へのアクセスでHome.vueが表示
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
          children: [
            {
              path: 'cards/:cardId',
              component: CardShow,
              props: route => ({
                cardId: parseInt(route.params.cardId, 10),
                boardId: parseInt(route.params.boardId, 10),
              }),
              meta: {
                ws: route => route.path.split('/cards')[0],
              },
            },
          ],
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
