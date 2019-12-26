django-vue-template
-------------------

* Django 2.1
* Django channels 2.1
* Vue
* Vuex
* vue/cli@4.1.1

###### 参考記事
[DjangoとVueでカンバンアプリケーションを作る](https://qiita.com/denzow/items/046f3c8b9bd8d3378eb4)

### 環境構築
```
git clone https://github.com/gamogamola/django_vue_test.git
cd django_vue_test
pipenv install --python 3.6
touch .env
cd /app/application/vuejs
touch .env.vuejs
cd
```

```
docker-compose up -d
docker-compose exec service python manage.py createsuperuser
docker-compose exec service python manage.py migrate
```

### モデル作成
```
docker-compose exec service python manage.py makemigrations { アプリ名 }
```

#### websocket通信テスト
```
pipenv shell
python wstest.py
```

#### デバッグ
* 動作がおかしい時
```
docker-compose restart
```
* 環境依存関係でエラーが出る場合の最終手段
```
docker-compose logs vuejs | less

docker-compose run vuejs sh

rm -rf node_modules package-lock.json && npm install
```

## メモ

##### カードの並び順の更新流れ

1. Component_vuejs/src/store/pages/boards.py_から`updateCardOrder(action)`を呼び出し
1. ( ___vies/ws/kanban_consumer.py___ ) Websocket経由で情報の更新をサーバにリクエスト
1. サーバ側がWebsocketで新しいカードの並び順(正確にばボード全体のデータ)を返送し
1. ( ___vuejs/src/store/pages/boards.py___ ) `setBoardData(mutation)`が実行される
  - Component側で、D&Dが完了するのは1.だが、新しい並び順になるのは4.まで完了した時点
    - そのため、その間はD&Dが完了しても、その前のデータがレンダリングされてしまうのでチラツキが発生
    - Websocketではサーバが次のメッセージを戻すまで待つといったことができない
      - 対策として、処理を実行したクライアントではサーバのメッセージを待たずにデータを更新する
      - _vuejs/src/store/pages/board.js_
        ~~~javascript
        commit('updateCardOrder', { pipeLineId, cardList });
        ...
        updateCardOrder(state, { pipeLineId, cardList }) { // あるPipeLine内の並びだけ更新する
          const targetPipeLine = state.boardData.pipeLineList.find(pipeLine => pipeLine.pipeLineId === pipeLineId);
          targetPipeLine.cardList = cardList;
        },
        ...
        ~~~
      - `updateCardOrder(mutation)`を追加し、`updateCardOrder(action)`内でサーバにリクエスした直後に
      `commit('updateCardOrder', { pipeLineId, cardList })`を呼び出し
      サーバの返答を待たずに自身のStore内のデータだけは更新する

##### ブラウザ間のデータ同期
Channelsでブラウザをまたがってメッセージの送受信をするにはChannelLayerというコンポーネントを使用
Websocketの接続ごとに生成されるConsumerインスタンスはChannelLayerを通じて相互にメッセージ受信ができるようになる
1. ChannelLayerを有効化にする
    - `CHANNEL_LAYERS`をsettingsに追加(バックエンドをRedisにする)
1. ConsumerにChannelLayerの初期化を追加
    - ( ___views/ws/kanban_consumer.py___ ) Consumerが初期化されるタイミングで、ConsumerをChannelLayerに追加
    - ChannelLayerは、チャットにおけるルームのような概念で、どのルームに所属するかを指定して初期化
    - URLに含まれている`board_id`をルーム名として使って`group_add`を行う
    - ChannelLayer関連の処理は非同期になっているので、同期Consumer内で使う場合は___`async_to_sync`デコレータを使って同期処理に変換___
1. ブロードキャスト処理の実装
    - ( ___views/ws/kanban_consumer.py___ ) `self.channel_layer.group_send`の第一引数でどのグループに
    メッセージを通知するかを指定するので自身と同じ`room_group_name`を指定
    第二引数にはメッセージ内容を指定`type:`に文字列で指定したメソッド名が各Consumerで呼び出される
    - つまり受け取ったConsumer(送信元自身のConsumerも含む)がtypeに指定された`send_board_data`が呼び出され
    それぞれのConsumerに紐付いたClientに新しいボードデータを戻す

##### 2つのブラウザで開いてるときの例
1. Client1がカード並び替えを実行
1. Consumer1が新しい並びでカードを更新
1. Consumer1が同じGroupに所属するConsumerにメッセージを送信
1. Consumer1,Consumer2がメッセージを受信
1. Consumer1がClient1,Consumer2がClient2に新しい並びでのボードデータを送信
1. Client1,Client2が新しい並びで再レンダリング


##### Card追加のロジック
1. CardはPipeLine内での位置をorderという属性で管理しているので、追加時はその最大のorderよりも大きい値をセット
    - orderは連番であることを期待しているので、単にCardの数+1
      1. ( ___modules/kanban/models/card.py___ ) `get_current_card_count_by_pipe_line`でPipeLine内のCard数を取得
      1. ( ___modules/kanban/service.py___ ) `add_card`で、現在のカード数 + 1
        - ( ___views/api/boards.py___ ) add_card用のAPI `class CardApi`
          - ( ___views/urls.py___ )cardTitleとpipeLineIdをパラメータとしてとる
1. フロント側からサーバサイドへアクセスする際に利用するAPIClient(KanbanClient)の`addCard`メソッドで`api/cards`にアクセス
    - ( ___vuejs/utils/kanbanClient.js___ ) `addCard({ cardTitle, pipeLineId })`
    - ( ___vuejs/src/store/pages/board.js___ ) `async addCard`
    - ( ___vuejs/src/pages/Board/components/BoardArea/PipeLine.vue___ )
1. Card追加完了後にデータ再取得
    - ( ___views/ws/kanban_consumer.py___ ) `broadcast_board_data`というメッセージを
    サーバ側に送信することで同じボードを開いている全クライアントのデータが更新
