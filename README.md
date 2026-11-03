# web-http-lab
HTTP и FastAPI

## Установка зависимостей
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
## Запуск

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

 
## Проверка после запуска

Открыть в браузере:

- http://127.0.0.1:8000/health — `GET /health`, проверка, что приложение работает
- http://127.0.0.1:8000/hello — `GET /hello`, приветствие
- http://127.0.0.1:8000/docs — здесь можно проверить маршруты

## Заметки

- `GET /notes` — список сохранённых заметок. Если заметок нет, вернётся `[]`.
- `POST /notes` — принимает заголовок `title` и текст `content`, создаёт заметку с `id` и возвращает статус `201`.
- `GET /notes/{note_id}` — показывает одну заметку по её `id`. Если заметки нет, вернётся `404` и `{"detail":"Note not found"}`.





Пример запроса `POST /notes`:


```json
{"title": "Покупки", "content": "Купить корм"}
```

Ответ `201`, если это первая заметка после запуска:

```json
{"id": 1, "title": "Покупки", "content": "Купить корм"}
```

Заметки хранятся в памяти и исчезают после перезапуска приложения
