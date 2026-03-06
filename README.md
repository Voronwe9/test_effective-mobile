# Backend тестовое (DRF + PostgreSQL)

## Что реализовано

### 1) Модуль взаимодействия с пользователем
- `POST /api/auth/register/` — регистрация (ФИО, email, пароль, повтор пароля)
- `POST /api/auth/login/` — вход по email + password, выдается собственный токен (`AuthToken`)
- `POST /api/auth/logout/` — logout (текущий токен помечается revoked)
- `GET /api/auth/profile/` — получить профиль
- `PATCH /api/auth/profile/` — обновить профиль
- `POST /api/auth/delete/` — мягкое удаление аккаунта (`is_active=False` + revoke всех токенов)

Идентификация после логина выполнена через заголовок:
`Authorization: Token <token>`

### 2) Собственная система разграничения доступа (RBAC)

Схема таблиц:

1. `accounts_user` — пользователь системы.
2. `accounts_authtoken` — собственная таблица сессий/токенов.
3. `access_control_role` — роль (`admin`, `manager`, `analyst`).
4. `access_control_action` — действие (`read`, `manage`).
5. `access_control_resource` — ресурс (`orders`, `reports`, `access_rules`).
6. `access_control_rolepermission` — правило доступа `role + resource + action -> allow/deny`.
7. `access_control_userrole` — назначение ролей пользователям.

Проверка доступа выполняется функцией:
- `access_control.services.user_has_access(user, resource_code, action_code)`

Логика ответов:
- пользователь не определен (нет/невалидный токен) → `401`
- пользователь определен, но нет доступа к ресурсу → `403`

### 3) API управления правами для администратора
Маршруты в `/api/access/`:
- `/roles/`
- `/actions/`
- `/resources/`
- `/permissions/`
- `/user-roles/`

Доступ к ним только при наличии права `manage` на ресурс `access_rules`.

### 4) Mock бизнес-объекты
- `GET /api/business/orders/` — ресурс `orders`, действие `read`
- `GET /api/business/reports/` — ресурс `reports`, действие `read`

## Переменные окружения (`.env` + dotenv)
Настройки полностью вынесены в `.env`, загрузка выполняется через `python-dotenv` в `config/settings.py`.

Пример есть в `.env.example`:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

## Docker

### Запуск
1. Скопировать шаблон:
   - `cp .env.example .env`
2. Поднять сервисы:
   - `docker compose up --build`
3. API будет доступно на `http://localhost:8000`

Сервисы:
- `web` — Django приложение
- `db` — PostgreSQL

## Тестовые данные (минимальные)
Добавить в БД:
- Роли: `admin`, `manager`
- Actions: `manage`, `read`
- Resources: `access_rules`, `orders`, `reports`
- RolePermission:
  - `admin` -> `access_rules/manage` (allow)
  - `admin` -> `orders/read` (allow)
  - `admin` -> `reports/read` (allow)
  - `manager` -> `orders/read` (allow)

Создайте пользователя-админа и свяжите его с ролью `admin` через `UserRole`.
