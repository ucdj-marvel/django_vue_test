django-vue-template
-------------------


* Django 2.1
* Django channels 2.1
* Vue
* Vuex
* vue/cli@4.1.1

### ??
```
git clone
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

### ??????
```
docker-compose exec service python manage.py makemigrations { ???? }
```

### vuejs????????
```
docker-compose logs vuejs | less

docker-compose run vuejs sh

rm -rf node_modules package-lock.json && npm install
```

#### websocket?????
```
pipenv shell
python wstest.py
```
