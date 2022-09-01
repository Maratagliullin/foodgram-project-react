# Проект Продуктовый помошник 

![CI](https://github.com/Maratagliullin/foodgram-project-react/actions/workflows/yamdb_workflow.yaml/badge.svg)
Проект расположен по адресу http://yandexpracticum.hopto.org/

Дипломный проект — сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. 

## Техническое описание проекта Foodgram
К проекту по адресу http://yandexpracticum.hopto.org/api/docs/redoc.html подключена документация API Foodgram. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

## Ресурсы API Foodgram

#### Ресурс **users**: пользователи.  
Алгоритм регистрации, получения токена, изменения пароля пользователей описан в документации адресу http://yandexpracticum.hopto.org/api/docs/redoc.html 

---
#### Ресурс **recipes**: список рецептов.   
**Получение списка всех рецептов:**  
Тип запроса **GET**,  http://yandexpracticum.hopto.org/api/recipes/
Права доступа: **Доступно без токена**  

**Пример ответа:**
```json
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

**Добавление рецепта:**  
Тип запроса **POST**,  http://yandexpracticum.hopto.org/api/recipes/
Права доступа: **Авторизованные пользователи**  

**Параметры запроса:**  
**ingredients** - Список ингредиентов (массив объектов, обязательное)  
**tags** - Список id тегов (массив объектов, обязательное)
**image**	- Картинка (Картинка, закодированная в Base64, обязательное)  
**name** - Название (тим срока, обязательное)  
**text** - Описание (тип строка, обязательное)
**cooking_time** - Время приготовления  (тип число, обязательное)      

**Пример запроса:**
```json
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

**Поддерживаются следующие типы операций:**  
Получение списка всех рецептов  
Добавление рецепта  
Получение информации о рецепте  
Частичное обновление информации о рецепте  
Удаление рецепта  

---
#### Ресурс **tags**: теги (типы) рецептов («Завтрак», «Обед», «Ужин»).  
**Получение списка всех тегов:**  
Тип запроса **GET**,  http://yandexpracticum.hopto.org/api/recipes/
Права доступа: **Доступно без токена**  

**Пример ответа:**
```json
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
```

**Подерживаются следующие типы операций:**  
Получение списка всех тегов  
Получение конкретного тега

---
#### Ресурс **shopping_cart**: список покупок. Скачивание файла со списком покупок. 
Тип запроса **GET**,  http://yandexpracticum.hopto.org/api/recipes/download_shopping_cart/ 
Права доступа: **Авторизованные пользователи**  

**Пример ответа:**
Загрузка txt документа со списком ингредиентов

**Подерживаются следующие типы операций:**  
Скачивание списка рецептов
Добавление рецепта в список покупок
Удаление рецепта из списка покупок

---
#### Ресурс **favorites**: Избранное. Добавление рецепта в избранное.  
**Добавить рецепт в избранное:**  
Тип запроса **POST**,  http://yandexpracticum.hopto.org/api/recipes/{id}/favorite/  
Права доступа: **Авторизованные пользователи**  

**Параметры запроса:**  
**id** - ID рецепта (тип число, обязательное)  

**Пример ответа:**
```json
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```
**Подерживаются следующие типы операций:**  
Добавление рецепта в избранное
Удаление рецепта из избранного

---
#### Ресурс **ingredients**: Ингредиенты . 
**Список ингредиентов с возможностью поиска по имени.**  
Тип **GET**, http://yandexpracticum.hopto.org/api/ingredients/
Права доступа: **Все пользователи**  

**Параметры запроса:** 
**name** -Поиск по частичному вхождению в начале названия ингредиента. (тип строка)   

**Пример ответа:**
```json
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

**Получение ингредиента по id.**  
Тип **GET**, http://yandexpracticum.hopto.org/api/ingredients/{id}/
Права доступа: **Все пользователи**  

**Параметры запроса:** 
**id** - Уникальный идентификатор этого ингредиента. (тип число)   

**Пример ответа:**
```json
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

---
#### Ресурс **subscriptions**: подписки . 
**Возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты:**  
Тип **GET**, http://yandexpracticum.hopto.org/api/users/subscriptions/
Права доступа: **Авторизованные пользователи**  

**Параметры запроса:** 
**page** - Номер страницы. (тип число, обязательное)   
**limit** - Количество объектов на странице (тип число, обязательное)  
**recipes_limit** - Количество объектов внутри поля recipes. (тип число, обязательное)

**Пример ответа:**
```json
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
```

**Подписаться на пользователя:**  
Тип **POST**, http://yandexpracticum.hopto.org/api/users/{id}/subscribe/
Права доступа: **Аутентифицированные пользователи**  

**Параметры запроса:**    
**id** - Уникальный идентификатор этого пользователя. (тип число, обязательное)  

**Пример ответа:**
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**Отписаться от пользователя:**  
Тип **POST**, http://yandexpracticum.hopto.org/api/users/{id}/subscribe/
Права доступа: **Аутентифицированные пользователи**  

**Параметры запроса:**    
**id** - Уникальный идентификатор этого пользователя. (тип число, обязательное)  

**Пример ответа:**
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.**

## Инструкция
### Предварительные действия:
Установка Docker - официальное руководство: https://docs.docker.com/get-docker/

Корректность установки необходимо проверить командой в терминале:

 ```docker --version```  

**Вывод:**  
 ```
Docker version 20.10.14, build a224086, build f0df350 - версия докер и номер сборки может отличаться
 ```
Установка Docker-compose - официальное руководство:  https://docs.docker.com/compose/

Корректность установки необходимо проверить командой в терминале:

 ```docker-compose --version ```  

**Вывод:**  
 ```
 Docker Compose version v2.0.0-beta.6   
 ```

### Локальный запуск проекта:

Расположение проекта на github: https://github.com/Maratagliullin/foodgram-project-react

Необходимо склонировать репозиторий перейти в директорию проекта (дирректория infra) и запустить сборку командой:

```docker-compose build```  

Запуск проекта (команда):

```docker-compose up -d```  

#### Интерфейсы приложения:
Административный интерфейс Django:   
http://yandexpracticum.hopto.org/admin

**Учетные данные:**.    
http://yandexpracticum.hopto.org/admin/login  
Администратор:   
Логин: admin@admin.ru  
Пароль: adminpass  

http://yandexpracticum.hopto.org/signin 
Пользователь:  
Логин: user@user.ru 
Пароль: userpass 

Документация API Foodgram:  
http://yandexpracticum.hopto.org/api/docs/redoc.html 

Учетные данные к сервисам расположены в .env файле в директории проекта. Фаил .env необходимо создать в диррктории infra и заполнить самостоятельно.  

### Пример перечня переменных окружения:     
#####  Движок базы данных:
**DB_ENGINE**=django.db.backends.postgresql
##### Имя базы данных:
**DB_NAME**=postgres 
##### Логин для подключения к базе данных:
**POSTGRES_USER**=postgres 
##### Пароль для подключения к БД (установите свой):
**POSTGRES_PASSWORD**=postgres 
##### Название сервиса (контейнера):
**DB_HOST**=db 
##### Порт для подключения к БД: 
**DB_PORT**=5432 
##### Имя суперпользователя (установите свой):
**DJANGO_SUPERUSER_USER**=administrator
##### Email суперпользователя (установите свой):
**DJANGO_SUPERUSER_EMAIL**=admin@admin.ru
##### Пароль суперпользователя (установите свой):
**DJANGO_SUPERUSER_PASSWORD**=adminpass
##### Пример секретного ключа django, 50 знаков (установите свой): 
**SECRET_KEY**=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs 


Учетные данные

