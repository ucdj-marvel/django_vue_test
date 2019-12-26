django-vue-template
-------------------


* Django 2.1
* Django channels 2.1
* Vue
* Vuex
* vuecli 3

??
-------------------
```touch .env
vim .env
edit DJANGO_ENV```

```docker-compose up -d
docker-compose exec service python manage.py createsuperuser
docker-compose exec service python manage.py migrate```

????????????
-------------------
```docker-compose exec service python manage.py makemigrations { ???? }```

????
-------------------
```docker-compose logs vuejs | less

docker-compose run vuejs sh

rm -rf node_modules package-lock.json && npm install```
