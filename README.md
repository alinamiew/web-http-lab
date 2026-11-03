# web-http-lab

## Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload
```

## Проверка после запуска

Открыть в браузере:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/hello
- http://127.0.0.1:8000/docs





HTTP и FastAPI

## Заметки
`GET /notes` список сохранённых заметок
`POST /notes` заголовок `title` и текст `content`, создаёт заметку с `id` и возвращает статус `201`
