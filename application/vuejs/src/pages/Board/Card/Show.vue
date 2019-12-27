<template>
  <div class="modal" aria-labelledby="modal-title" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal-title">
            <span>
              {{ focusedCard.title }}
            </span>
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p class="card-content">{{ focusedCard.content }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger">delete</button>
          <button type="button" class="btn btn-primary">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapState, mapActions } = createNamespacedHelpers('board');


export default {
  name: 'CardShow',
  props: {
    cardId: {
      type: Number,
      default: null,
    },
    boardId: {
      type: Number,
      default: null,
    },
  },
  computed: {
    ...mapState(['focusedCard']),
  },
  methods: {
    ...mapActions([
      'fetchFocusedCard',
    ]),
  },
  watch: {
    cardId: {
      immediate: true,
      handler(cardId) {
        console.log(cardId);
        this.fetchFocusedCard({
          boardId: this.boardId,
          cardId,
        });
      },
    },
  },
};
</script>

<style lang='scss' scoped>
  .modal {
    display: block;
    background-color: rgba(1, 1, 1, 0.5);
  }
  .modal-dialog {
    z-index: 1060;
  }
  .edit-area {
    width: 95%;
    height: 5rem;
  }
  .empty-content {
    text-decoration: underline;
    cursor: pointer;
  }
  .card-content {
    white-space: pre;
  }
</style>
