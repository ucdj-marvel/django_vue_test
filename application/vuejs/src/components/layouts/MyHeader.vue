<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand" to="/">KANBAN</router-link>

    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <!-- ログインしている場合 -->
      <ul class="navbar-nav ml-auto" v-if="isLoggedIn">
        <span class="navbar-text mr-1">Welcome to {{ accountInfo.name }}</span>
        <a class="btn btn-outline-primary" href="/accounts/logout/">Logout</a>
      </ul>
      <!-- ログインしていない場 -->
      <ul class="navbar-nav ml-auto" v-if="!isLoggedIn">
        <li class="nav-item">
          <a class="nav-link" href="#">Register</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Login</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
// 作成したActionをMyHeaderの初期化時に呼び出す
import { createNamespacedHelpers } from 'vuex';
const { mapState, mapActions } = createNamespacedHelpers('header');

export default {
  name: 'MyHeader',
  computed: {
    // ログインしているかどうかを示すため
    // accountInfoが空かを戻すisLoggedInというメソッドを定義
    isLoggedIn() {
      return this.accountInfo !== null;
    },
    // ...はスプレッド演算子
    // 指定した変数を展開して代入する
    ...mapState(['accountInfo']),  // Storeのstateとのマッピング
  },
  methods: {
    ...mapActions(['fetchAccountInfo']),  // StoreのActionsとのマッピング
  },
  // mapStateはcomputed、mapActionsはmethodsの中で使用
  created() {
    this.fetchAccountInfo();  // MyHeaderコンポーネントが初期化される際に実行される
  },
};
</script>

<style scoped>

</style>
