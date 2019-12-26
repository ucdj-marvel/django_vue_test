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
