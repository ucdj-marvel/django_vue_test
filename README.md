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

##### websocket通信テスト
```
pipenv shell
python wstest.py
```

##### デバッグ
-------------------
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
