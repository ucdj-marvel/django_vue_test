<template>
  <div class="pipe-line">
    <nav class="navbar navbar-dark">
      <span v-show="!isEditingPipeLineName">
        <span class="navbar-brand mb-0 h1 pipe-line-name"
              :class="{ 'waiting-rename' : isWaitingRename}"
              @dblclick="startPipeLineNameEdit">{{ pipeLineName }}</span>
        <span class="navbar-brand delete-pipe-line" data-toggle="tooltip" data-placement="top"
              title="delete pipeline" @click="delPipeLineAction">
           Del
        </span>
      </span>
      <span v-show="isEditingPipeLineName">
        <input type="text" v-model="editPipeLineName">
        <button type="button" class="btn btn-primary" @click="savePipeLineName">save</button>
      </span>
    </nav>
    <button class="add-card-button btn btn-block" @click="addCardAction">
      add card
    </button>
    <Draggable
      class="card-container"
      :options="options"
      v-model="wrappedCardList"
    >
      <Card v-for="card in wrappedCardList"
            class="item"
            :card="card"
            :key="card.cardId"
      />
    </Draggable>
  </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';
import Draggable from 'vuedraggable';
import Card from './Card.vue';

const { mapActions, mapGetters } = createNamespacedHelpers('board');

export default {
  name: 'PipeLine',
  components: {
    Draggable,
    Card,
  },
  // パイプラインの1列を表現するデータを
  // propsとして受け取り、それをもとに描画
  props: {
    pipeLine: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      options: {
        group: 'Cards',
        animation: 300,
        draggable: '.item',
      },
      isEditingPipeLineName: false,
      isWaitingRename: false,
      editPipeLineName: '',
    };
  },
  computed: {
    wrappedCardList: {
      get() {
        return this.pipeLine.cardList;
      },
      set(value) {
        console.log(value);
        this.updateCardOrder({
          pipeLineId: this.pipeLine.pipeLineId,
          cardList: value,
        });
      },
    },
    pipeLineName() {
      return this.pipeLine.name;
    },
  },
  watch: {
    pipeLine(newPipeLine, oldPipeLine) {
      if (newPipeLine.name !== oldPipeLine.name) {
        this.isWaitingRename = false;
      }
    },
  },
  methods: {
    addCardAction() {
      const cardTitle = window.prompt('CardTitle?');
      if (cardTitle) {
        this.addCard({
          pipeLineId: this.pipeLine.pipeLineId,
          cardTitle,
        });
      }
    },
    delPipeLineAction() {
      if (!window.confirm(`DELETE [${this.pipeLineName}] ? Are you sure?`)) return;
      this.deletePipeLine({
        boardId: this.getBoardId(),
        pipeLineId: this.pipeLine.pipeLineId,
      });
    },
    startPipeLineNameEdit() {
      this.isEditingPipeLineName = true;
      this.editPipeLineName = this.pipeLine.name;
    },
    async savePipeLineName() {
      this.isEditingPipeLineName = false;
      if (this.editPipeLineName === this.pipeLine.name) return;
      await this.renamePipeLine({
        pipeLineId: this.pipeLine.pipeLineId,
        pipeLineName: this.editPipeLineName,
      });
      // リネーム完了までのフラグ
      this.isWaitingRename = true;
    },
    // VueDraggableはD&D終了時に、v-modelに指定したwrappedCardListのsetを呼び出す
    // その中でupdateCardOrderを呼び出してやれば新しい並び順を渡すことができる
    ...mapActions([
      'updateCardOrder',
      'addCard',
      'renamePipeLine',
      'deletePipeLine',
    ]),
    ...mapGetters([
      'getBoardId',
    ]),
  },
};
</script>

<style lang='scss' scoped>
  .pipe-line {
    margin-right: 1rem;
    width: 15rem;
  }
  .pipe-line-name {
    cursor: pointer;
    font-size: 1rem;
  }
  .navbar {
    background-color: #6f7180;
  }
  .waiting-rename {
    color: rgba(0, 0, 0, 0.3);
  }
  .card-container {
    height: 100%;
  }
  .delete-pipe-line {
    cursor: pointer;
  }
  .add-card-button {
    cursor: pointer;
    text-align: center;
    background-color: #6f7180;
    color: #FFFFFF;
    border-color: #000;
    border-width: 2px;
    border-style: solid;
    border-radius: 25px 25px 55px 5px/5px 55px 25px 25px;
  }
</style>
