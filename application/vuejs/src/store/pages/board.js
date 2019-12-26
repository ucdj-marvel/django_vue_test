import camelcaseKeys from 'camelcase-keys';


const state = {
  boardData: {
    pipeLineList: [],
  },
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
  },
};

// Consumerから戻されたボードのデータをしまうためのstate.boardDataと
// 値をセットするためのsetBoardData mutationを定義
const mutations = {
  setBoardData(state, { boardData }) {
    // Pythonから来たデータをCamelCaseに変換
    state.boardData = camelcaseKeys(boardData, { deep: true });
  },
};


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
