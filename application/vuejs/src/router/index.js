import Vue from 'vue';
import Router from 'vue-router';
import WebSocketMiddleware from './middlewares/websocket';

import DefaultLayout from '../components/layouts/DefaultLayout.vue';
import NotFound from '../pages/NotFound.vue';
import Home from '../pages/Home/Index.vue';


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
        }
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
