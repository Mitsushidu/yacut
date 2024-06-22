# Yacut - сервис создания коротких ссылок
### Сервис Yacut позволит вам создать короткую версию вашей ссылки.
Реализованный функционал: создание связи между укороченным вариантом и оригинальной ссылкой, получение полной ссылки по короткому id.

## Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

    ```bash
    git clone 
    cd yacut
    ```

2. Cоздать и активировать виртуальное окружение:

    ```bash
    python3 -m venv venv
    source venv/scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

    ```bash
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. С помощью интерактивной оболочки Flask создать базу данных и таблицу URLmap:

    ```bash
    flask shell 
    >>> from yacut import db
    >>> db.create_all() 
    ```

5. Запустить проект на локальном сервере:

    ```bash
    flask run
    ```

## Примеры запросов:


1. **Эндпоинт: http://localhost/api/id/
   <br>Метод запроса: POST

    Запрос:

    * "url": "string" (required),
    * "custom_id": "string"(optional)

    Ответ:

    * "url": "string",
    * "short_link": "string"

    В ответе о создании связи между url и custom_id и короткую ссылку, предоставляющую доступ к оригинальной.
    >*Если не указать поле custom_id в запросе, то для него будет сгенерирована строка из шести случайных элементов. В качестве элементов будут использованы заглавные и строчные латинские буквы и цифры от 0 до 9.*

<br>

2. **Эндпоинт: http://localhost/api/id/{short_id}/
   <br>Метод запроса: GET

   Запрос:

   * "short_id ": "string" (required)
  
   Ответ:

   * "url": "string"

    В ответе будет возвращена полная оригинальная ссылка.

### Стек:

* flask = 2.0.2
* sqlalchemy = 1.4.29
* wtforms = 3.0.1
* alembic = 1.7.5

### Автор: mitsushidu
