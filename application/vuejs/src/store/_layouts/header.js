// 作成したAPI Clientを使う(Header用のStore)
// Vueはあるコンポーネント内に閉じた状態であれば
// そのコンポーネント内の変数として保持するだけでいいが
// コンポーネントをまたがったりする場合にはStoreというものを用意して、それを参照する
import KanbanClient from '../../../utils/kanbanClient';

// Storeはだいたい3つの要素を持つ

// state...現在のStoreの状態を示すもの
const state = {
  // 取得したアカウント情報を保持する必要がある
  accountInfo: null,
};

// actions...何らかの非同期を含む処理、最終的にmutationを呼び出すことが多い(stateを変更することは許されていない)
const actions = {
  // accountInfoに値をセットするには、作成したKanbanClient(APIClient)のgetAccountInfoを実行すれば良い
  async fetchAccountInfo({ commit }) {
    const accountInfo = await KanbanClient.getAccountInfo();
    commit('setAccountInfo', accountInfo);
  },
};

// mutations...stateへの変更処理。非同期処理を含んではならない
const mutations = {
  setAccountInfo(state, accountInfo) {
    state.accountInfo = accountInfo;
  },
};

// コンポーネントからはActionを呼び出し
// その結果をMutationに伝えてStateを更新する流れになることが多い


export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
