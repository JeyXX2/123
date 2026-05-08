# StudyHub

Веб-приложение на Flask для личного кабинета студента: регистрация и вход, заметки, загрузка файлов и простой REST API.

## Возможности

- Регистрация, авторизация и выход из аккаунта.
- Создание и удаление личных заметок.
- Загрузка, скачивание и удаление файлов.
- Хранение данных в SQLite через SQLAlchemy ORM.
- API для получения заметок текущего пользователя.
- Интерфейс на Bootstrap 5.

## Технологии

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite
- Bootstrap 5

## Быстрый старт

1. Клонировать репозиторий:
   ```bash
   git clone https://git.sourcecraft.dev/fus-serg/webserverapi.git
   cd webserverapi
   ```
2. Создать и активировать виртуальное окружение:
   - Windows (PowerShell):
     ```bash
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/macOS:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустить приложение:
   ```bash
   python run.py
   ```
5. Открыть в браузере:
   `http://127.0.0.1:5000`

## Структура проекта

```text
app/
  __init__.py          # инициализация Flask-приложения
  extensions.py        # подключение db и login manager
  forms.py             # WTForms формы
  models.py            # ORM модели
  routes.py            # web-маршруты и API
  templates/           # HTML шаблоны
run.py                 # точка входа
requirements.txt       # зависимости
```

## API

### `GET /api/my-notes`

Возвращает JSON со списком заметок авторизованного пользователя.

Пример ответа:

```json
{
  "user": "user@example.com",
  "notes": [
    {
      "id": 1,
      "title": "Конспект",
      "content": "Повторить Flask-Login",
      "created_at": "2026-04-29T08:00:00"
    }
  ],
  "count": 1
}
```

## Планы по развитию

- Редактирование заметок.
- Поиск и фильтрация по заметкам.
- Роли пользователей (user/admin).
- Покрытие тестами (pytest).
