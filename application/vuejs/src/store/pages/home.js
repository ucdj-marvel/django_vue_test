import KanbanClient from '../../../utils/kanbanClient';

const state = {
  boardList: [],
};

// fetchBoardListのActionを実行すると
// 最終的にstate.boardListの中にそのユーザが作成したボード一覧が入る
const actions = {
  async fetchBoardList({ commit }) {
    const boardList = await KanbanClient.getBoardList();
    commit('setBoardList', { boardList });
  },
};

const mutations = {
  setBoardList(state, { boardList }) {
    state.boardList = boardList;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
