# web-http-lab

HTTP и FastAPI

## Подготовка базы

Установить PostgreSQL 18 и pgAdmin 4. При установке оставить порт 5432 и запомнить пароль пользователя postgres. Служба PostgreSQL должна быть запущена.

В pgAdmin открыть сервер PostgreSQL и создать базу web_http_lab: правой кнопкой на Databases → Create → Database.

Выбрать эту базу, открыть Query Tool, вставить SQL из schema.sql и выполнить. Таблицу нужно создать один раз в новой базе.

## Установка зависимостей

В терминале PowerShell в папке проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Подключение к базе

В том же терминале задать переменные:

```powershell
$env:DATABASE_URL = 'postgresql://postgres:YOUR_PASSWORD@localhost:5432/web_http_lab'
$env:PSYCOPG_IMPL = 'python'
```

Вместо YOUR_PASSWORD поставить свой пароль postgres. Если в пароле есть специальные символы, их нужно закодировать для URL. Настоящий пароль в файлы проекта и на GitHub не добавлять. После открытия нового терминала переменные нужно задать заново.

Используется Python-версия psycopg и библиотеки установленного PostgreSQL. В main.py указан путь C:\Program Files\PostgreSQL\18\bin. Эти шаги запуска рассчитаны на Windows и PostgreSQL 18 в этой папке. Если PostgreSQL установлен в другом месте, путь в main.py нужно поменять.

## Запуск

В том же терминале:

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

Пример ответа `201` (id выдаёт база):

```json
{"id": 1, "title": "Покупки", "content": "Купить корм"}
```

Заметки хранятся в PostgreSQL и остаются после перезапуска приложения.

Для проверки создать заметку через POST в /docs и запомнить её id. Остановить приложение через Ctrl+C, запустить снова и получить заметку через GET /notes/{note_id}. Должен вернуться статус 200 и та же заметка.
