<template>
  <div class="pipe-line">
    <nav class="navbar navbar-dark">
      <span>
        <span class="navbar-brand mb-0 h1 pipe-line-name">{{ pipeLineName }}</span>
        <span class="navbar-brand delete-pipe-line" data-toggle="tooltip" data-placement="top"
              title="delete pipeline" @click="delPipeLineAction">
          (-)
        </span>
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
      window.confirm(`DELETE [${this.pipeLineName}] ? Are you sure?`);
    },
    // VueDraggableはD&D終了時に、v-modelに指定したwrappedCardListのsetを呼び出す
    // その中でupdateCardOrderを呼び出してやれば新しい並び順を渡すことができる
    ...mapActions([
      'updateCardOrder',
      'addCard',
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
