# web-http-lab

HTTP и FastAPI. Заметки хранятся в PostgreSQL.

## Подготовка базы

Установить PostgreSQL 18 и pgAdmin 4. При установке оставить порт 5432 и запомнить пароль пользователя postgres. Служба PostgreSQL должна быть запущена.

В pgAdmin открыть сервер PostgreSQL и создать базу web_http_lab: правой кнопкой на Databases → Create → Database.

Выбрать эту базу, открыть Query Tool, вставить SQL из schema.sql и выполнить. Таблицу нужно создать один раз в новой базе.

## Запуск через Docker

Открыть Docker Desktop и дождаться Engine running. PostgreSQL работает на компьютере отдельно от контейнера.

В терминале PowerShell в папке проекта собрать образ:

```powershell
docker build -t notes-api:0.1 .
```

Задать подключение к базе:

```powershell
$env:DATABASE_URL = 'postgresql://postgres:YOUR_PASSWORD@host.docker.internal:5432/web_http_lab'
```

Вместо YOUR_PASSWORD поставить свой пароль postgres. Специальные символы в пароле нужно закодировать для URL. Настоящий пароль в файлы проекта и на GitHub не добавлять.

host.docker.internal — адрес компьютера из контейнера Docker Desktop. База web_http_lab и таблица notes должны быть созданы заранее.

Запустить контейнер в фоне:

```powershell
docker run -d --name notes-api -p 8000:8000 -e DATABASE_URL notes-api:0.1
```

Порт 8000 на компьютере должен быть свободен. Открыть http://localhost:8000/docs.

Посмотреть состояние и логи:

```powershell
docker ps -a
docker logs notes-api
```

Остановить контейнер и снова запустить:

```powershell
docker stop notes-api
docker start notes-api
```

Если контейнер notes-api уже существует, для повторного запуска использовать docker start. После изменения кода нужно снова собрать образ и пересоздать контейнер:

```powershell
docker build -t notes-api:0.1 .
docker stop notes-api
docker rm notes-api
docker run -d --name notes-api -p 8000:8000 -e DATABASE_URL notes-api:0.1
```

Перед созданием нового контейнера DATABASE_URL должна быть задана в текущем терминале. Заметки остаются в PostgreSQL при остановке и удалении контейнера API.

## Запуск без Docker на Windows

В терминале PowerShell в папке проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

В том же терминале задать переменные:

```powershell
$env:DATABASE_URL = 'postgresql://postgres:YOUR_PASSWORD@localhost:5432/web_http_lab'
$env:PSYCOPG_IMPL = 'python'
```

Вместо YOUR_PASSWORD поставить свой пароль. После открытия нового терминала переменные нужно задать заново.

Для запуска на Windows в main.py указан путь C:\Program Files\PostgreSQL\18\bin. Если PostgreSQL установлен в другом месте, этот путь нужно поменять. В Linux-контейнере эта настройка пропускается.

Запустить приложение:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Проверка после запуска

Открыть в браузере:

- http://localhost:8000/health — GET /health, проверка, что приложение работает
- http://localhost:8000/hello — GET /hello, приветствие
- http://localhost:8000/docs — здесь можно проверить маршруты

## Заметки

- GET /notes — список сохранённых заметок. Если заметок нет, вернётся [].
- POST /notes — принимает заголовок title и текст content, создаёт заметку с id и возвращает статус 201.
- GET /notes/{note_id} — показывает одну заметку по её id. Если заметки нет, вернётся 404 и {"detail":"Note not found"}.

Пример запроса POST /notes:

```json
{"title": "Покупки", "content": "Купить корм"}
```

Пример ответа 201 (id выдаёт база):

```json
{"id": 1, "title": "Покупки", "content": "Купить корм"}
```

В /docs создать заметку через POST, запомнить её id и получить через GET /notes/{note_id}. Должен вернуться статус 200 и та же заметка. Для отсутствующего id ожидается 404.

Заметки хранятся в PostgreSQL и остаются после перезапуска приложения. Для проверки перезапустить API или контейнер и получить заметку по прежнему id.


## Запуск через Docker Compose

Открыть Docker Desktop. Если старый контейнер notes-api занимает порт 8000, остановить его командой docker stop notes-api.

В папке проекта выполнить:

```powershell
docker compose up -d --build
docker compose ps -a
docker compose logs
```

Compose запускает API и PostgreSQL 16. API подключается к базе по имени db и ждёт её готовности через healthcheck. База notes, пользователь app и пароль app используются только для учебного запуска.

Таблица notes создаётся из schema.sql при первом запуске с пустым томом. Данные сохраняются в postgres_data. Это отдельная база: заметки из PostgreSQL на компьютере автоматически сюда не копируются.

Открыть http://localhost:8000/docs, создать заметку через POST /notes и получить её через GET /notes. Один /health не проверяет подключение к базе.

Остановить сервисы:

```powershell
docker compose down
```

Данные сохранятся. Для проверки снова выполнить docker compose up -d и получить ту же заметку. Команда docker compose down -v удаляет том вместе с данными.
