<template>
  <!-- @click="addBoardAction"でこのコンポーネント自体がクリックされた際に
       methodsに定義しているaddBoardActionを呼び出す -->
  <a href="#" @click="addBoardAction">
    <div class="card bg-dark text-white">
      <div class="card-body">
        <h5 class="card-title">Add Board()</h5>
      </div>
    </div>
  </a>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapActions } = createNamespacedHelpers('home');

export default {
  name: 'AddBoardCard',
  methods: {
    addBoardAction() {
      const boardName = window.prompt('BoardName?');
      if (boardName) {
        this.addBoard({
          boardName,
        });
      }
    },
    ...mapActions(['addBoard']),
  },
};
</script>
