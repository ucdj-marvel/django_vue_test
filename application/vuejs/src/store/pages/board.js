import _ from 'lodash';
import camelcaseKeys from 'camelcase-keys';

import kanbanClient from "../../../utils/kanbanClient";
import router from '../../router';


const state = {
  boardData: {
    pipeLineList: [],
  },
  focusedCard: {},  // 開いているカードの情報
  searchWord: '',  // 検索ワード
};

// WebSocketへの接続のstate.socketはrootのStoreの属性なので
// それにアクセスできるようにgetSocketというgetterを定義
const getters = {
  getSocket(state, getters, rootState) {
    return rootState.socket;
  },
  getFilteredPipeLineList(state) {
    const result = [];
    state.boardData.pipeLineList.forEach(pipeline => {
      const clonePipeLine = _.cloneDeep(pipeline);
      clonePipeLine.cardList = clonePipeLine.cardList.map(card => {
        const cloneCard = _.cloneDeep(card);
        const content = cloneCard.content !== null ? cloneCard.content : '';
        if (state.searchWord === null || state.searchWord === '') {
          cloneCard.isShown = true;
        } else {
          cloneCard.isShown = (
            cloneCard.title.toUpperCase().includes(state.searchWord.toUpperCase()) ||
            content.toUpperCase().includes(state.searchWord.toUpperCase())
          );
        }
        return cloneCard;
      });
      result.push(clonePipeLine);
    });
    return result;
  },
  getBoardId(state) {
    return state.boardData.boardId;
  },
};

const actions = {
  backToHome() {  // call from consumer
    router.push('/');
  },
  // ルーム内同期
  broadcastBoardData({ getters }) {
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'broadcast_board_data',
    });
  },
  setSearchWord({ commit }, searchWord) {
    commit('setSearchWord', searchWord);
  },
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
  // パイプラインの並び替え
  updatePipeLineOrder({ commit, getters }, { boardId, pipeLineList }) {
    console.log(boardId, pipeLineList);
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'update_pipe_line_order',
      boardId,
      pipeLineIdList: pipeLineList.map(x => x.pipeLineId),
    });
    commit('updatePipeLineOrder', { pipeLineList });
  },
  renameBoard({ getters }, { boardId, boardName }) {
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'rename_board',
      boardId,
      boardName,
    });
  },
  renamePipeLine({ getters }, { pipeLineId, pipeLineName }) {
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'rename_pipe_line',
      pipeLineId,
      pipeLineName,
    });
  },
  addCard({ getters }, { pipeLineId, cardTitle }) {
    console.log(pipeLineId, cardTitle);
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'add_card',
      pipeLineId,
      cardTitle,
    });
  },
  addPipeLine({ getters }, { boardId, pipeLineName }) {
    console.log(boardId, pipeLineName);
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'add_pipe_line',
      boardId,
      pipeLineName,
    });
  },
  deleteBoard({ getters }, { boardId }) {
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'delete_board',
      boardId,
    });
  },
  deletePipeLine({ getters }, { boardId, pipeLineId }) {
    console.log(boardId, pipeLineId);
    const socket = getters.getSocket;
    socket.sendObj({
      type: 'delete_pipe_line',
      boardId,
      pipeLineId,
    });
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

const mutations = {
  setBoardData(state, { boardData }) {
    // Pythonから来たデータをCamelCaseに変換
    state.boardData = camelcaseKeys(boardData, { deep: true });
  },
  // あるPipeLine内の並びだけ更新する
  updateCardOrder(state, { pipeLineId, cardList }) {
    const targetPipeLine = state.boardData.pipeLineList.find(pipeLine => pipeLine.pipeLineId === pipeLineId);
    targetPipeLine.cardList = cardList;
  },
  updatePipeLineOrder(state, { pipeLineList }) {
    state.boardData.pipeLineList = pipeLineList;
  },
  setFocusedCard(state, cardData) {
    state.focusedCard = cardData;
  },
  setSearchWord(state, searchWord) {
    state.searchWord = searchWord;
  },
};


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
