import camelcaseKeys from 'camelcase-keys';
import kanbanClient from "../../../utils/kanbanClient";


const state = {
  boardData: {
    pipeLineList: [],
  },
  focusedCard: {},  // 開いているカードの情報
};

// WebSocketへの接続のstate.socketはrootのStoreの属性なので
// それにアクセスできるようにgetSocketというgetterを定義
const getters = {
  getSocket(state, getters, rootState) {
    return rootState.socket;
  },
  getFilteredPipeLineList(state) {
    return state.boardData.pipeLineList;
  },
  getBoardId(state) {
    return state.boardData.boardId;
  },
};

const actions = {
  // ルーム内同期
  broadcastBoardData({ getters }) {
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'broadcast_board_data',
    });
  },
  // Consumerのupdate_card_orderをStoreから呼び出せるように定義
  // 更新対象のpipeLineIdと新しい並び順になったカードの一覧をcardListとして受け取る
  updateCardOrder({ commit, getters }, { pipeLineId, cardList }) {
    console.log(pipeLineId, cardList);
    // rootStoreに格納されているWebSocketのコネクションを取得
    const socket = getters.getSocket;
    // サーバに対してsendObjでtype: update_card_orderを含んだメッセージを送信
    socket.sendObj({
      type: 'update_card_order',
      pipeLineId,
      cardIdList: cardList.map(x => x.cardId),
    });
    commit('updateCardOrder', { pipeLineId, cardList });
  },
  async addCard({ dispatch }, { pipeLineId, cardTitle }) {
    await kanbanClient.addCard({
      pipeLineId,
      cardTitle,
    });
    dispatch('broadcastBoardData');
  },
  async fetchFocusedCard({ commit }, { boardId, cardId }) {
    const cardData = await kanbanClient.getCardData({ boardId, cardId });
    commit('setFocusedCard', cardData);
  },
  async updateCardContent({ commit }, { boardId, cardId, content }) {
    const cardData = await kanbanClient.updateCardData({
      boardId,
      cardId,
      content,
    });
    commit('setFocusedCard', cardData);
  },
  async updateCardTitle({ commit, dispatch }, { boardId, cardId, title }) {
    const cardData = await kanbanClient.updateCardData({
      boardId,
      cardId,
      title,
    });
    commit('setFocusedCard', cardData);
    // titleはボード自体に出ているので他のクライアントへの反映を依頼する必要がある
    dispatch('broadcastBoardData');
  },
  async deleteCard({ dispatch }, { boardId, cardId }) {
    await kanbanClient.deleteCard({
      boardId,
      cardId,
    });
    // カード自体はボード自体に出ているので他のクライアントへの反映を依頼する必要がある
    dispatch('broadcastBoardData');
  },
};

// Consumerから戻されたボードのデータをしまうためのstate.boardDataと
// 値をセットするためのsetBoardData mutationを定義
const mutations = {
  updateCardOrder(state, { pipeLineId, cardList }) { // あるPipeLine内の並びだけ更新する
    const targetPipeLine = state.boardData.pipeLineList.find(pipeLine => pipeLine.pipeLineId === pipeLineId);
    targetPipeLine.cardList = cardList;
  },
  setBoardData(state, { boardData }) {
    // Pythonから来たデータをCamelCaseに変換
    state.boardData = camelcaseKeys(boardData, { deep: true });
  },
  setFocusedCard(state, cardData) {
    state.focusedCard = cardData;
  },
};


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
