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
  // stateを更新せず、ボードの追加が完了したら
  // dispatch('fetchBoardList');で
  // fetchBoardListアクションを呼び出し、ボード一覧の再取得
  async addBoard({ dispatch }, { boardName }) {
    await KanbanClient.addBoard({ boardName });
    dispatch('fetchBoardList');
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
