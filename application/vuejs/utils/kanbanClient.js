// APIにアクセスするユーティリティ(API Client)
// javascriptのHTTPClientライブラリ
import axios from 'axios';
import { loadProgressBar } from 'axios-progress-bar';
import camelcaseKeys from 'camelcase-keys';


const _handleSuccess = response => {
  console.log(response.data);
  // すべてのJSONのキーをスネークケースからキャメルケースに変換する
  response.data = camelcaseKeys(response.data, { deep: true });
  return response;
};

class Client {
  constructor() {
    this.service = axios.create();
    this.service.interceptors.response.use(_handleSuccess);
    loadProgressBar({ showSpinner: false }, this.service);
  }

  _get(path, payload) {
    return this.service.get(path, payload);
  }

  _patch(path, payload) {
    return this.service.patch(path, payload);
  }

  _post(path, payload, config = {}) {
    return this.service.post(path, payload, config);
  }

  _put(path, payload) {
    return this.service.put(path, payload);
  }

  _delete(path) {
    return this.service.delete(path);
  }
}

class KanbanClient extends Client {
  constructor() {
    super();
    this.baseUrl = '/api';
  }
  async getAccountInfo() {
    const response = await this._get(`${this.baseUrl}/accounts/`);
    return response.data.accountInfo;
  }
  // Boardの一覧取得
  async getBoardList() {
    const response = await this._get(`${this.baseUrl}/boards/`);
    return response.data.boardList;
  }
  // Boardの追加
  async addBoard({ boardName }) {
    await this._post(`${this.baseUrl}/boards/`, {
      boardName,
    });
  }
  // カードの追加
  async addCard({ cardTitle, pipeLineId }) {
    await this._post(`${this.baseUrl}/cards/`, {
      cardTitle,
      pipeLineId,
    });
  }
  // モーダルで表示するカードのAPI呼び出し
  async getCardData({ boardId, cardId }) {
    const response = await this._get(`${this.baseUrl}/boards/${boardId}/cards/${cardId}/`);
    return response.data.cardData;
  }
  // カードの更新
  async updateCardData({
    boardId,
    cardId,
    content,
    title,
  }) {
    const response = await this._patch(`${this.baseUrl}/boards/${boardId}/cards/${cardId}/`, {
      content,
      title,
    });
    return response.data.cardData;
  }
  // カードの削除
  async deleteCard({ boardId, cardId }) {
    await this._delete(`${this.baseUrl}/boards/${boardId}/cards/${cardId}/`);
  }
}
// getAccountInfoを呼び出すと/api/accounts/にアクセスし
// その結果をキャメルケースに変換したものが戻される

export default new KanbanClient();
