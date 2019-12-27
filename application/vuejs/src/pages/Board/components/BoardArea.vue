<template>
  <div class="board-area">
    <!-- Draggableのv-modelで指定した属性に対してsetterが呼び出されるため
         mapStateでStoreのstateを直接使うのではなく、
         setを定義したComputedを別で(wrappedPipeLineList)実装する必要がある -->
    <Draggable
      v-model="wrappedPipeLineList"
      class="board-container"
      :options="options"
    >
      <PipeLine
        v-for="pipeLine in wrappedPipeLineList"
        :pipeLine="pipeLine"
        class="pipe-line-item"
        :key="pipeLine.id"
      />
    </Draggable>
    <router-view></router-view>
  </div>
</template>

<script>
// VueDraggableをインポート
// これにより簡単に要素のドラッグアンドロップが実装できる
import Draggable from 'vuedraggable';
import { createNamespacedHelpers } from 'vuex';

import PipeLine from './BoardArea/PipeLine.vue';

const { mapGetters } = createNamespacedHelpers('board');


export default {
  name: 'BoardArea',
  components: {
    Draggable,
    PipeLine,
  },
  data() {
    return {
      // VueDraggableのオプション属性で
      // draggableは指定したクラスをもった要素のみがドラッグ可能になる
      // これでドラッグさせたくない要素との混合が可能に
      options: {
        animation: 300,
        draggable: '.pipe-line-item',
      },
    };
  },
  computed: {
    wrappedPipeLineList: {
      get() {
        // ボードの構成情報はgetFilteredPipeLineListで取得
        return this.getFilteredPipeLineList;
      },
      set(value) {
        console.log('update', value);
      },
    },
    ...mapGetters([
      'getFilteredPipeLineList',
      'getBoardId',
    ]),
  },
  methods: {
  },
};
</script>

<style scoped>
.board-area {
  margin: 1rem 0;
  width: 100%;
}
.board-container {
  display: flex;
}
</style>
