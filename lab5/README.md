# Game Store API

![CI Pipeline](https://github.com/feardelans/refactoring/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)

REST API бекенд для магазину відеоігор (аналог Steam), побудований на Flask з архітектурою Controller-Service-Repository та покриттям юніт-тестами.

## Архітектура

Проєкт дотримується шаблону **Controller → Service → Repository**:

| Шар | Призначення |
|-----|-------------|
| **`models/`** | Dataclass-сутності (`User`, `Game`, `Review`) |
| **`repositories/`** | Доступ до даних (in-memory сховище) |
| **`services/`** | Бізнес-логіка, валідація |
| **`controllers/`** | Точки входу (legacy CLI-контролери) |
| **`app.py`** | Flask REST API, що обгортає сервіси |

## Структура каталогів

```text
lab5/
├── app.py                     # Flask REST API
├── Dockerfile                 # Образ додатку
├── Dockerfile.test            # Образ для тестів
├── docker-compose.yaml        # App + PostgreSQL
├── requirements.txt           # Залежності Python
├── .github/workflows/ci.yml   # CI/CD конвеєр
├── src/
│   ├── controllers/
│   │   ├── store_controller.py
│   │   └── user_controller.py
│   ├── models/
│   │   ├── user.py
│   │   ├── game.py
│   │   └── review.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── game_repository.py
│   └── services/
│       ├── store_service.py
│       └── user_service.py
└── tests/
    ├── test_store_service.py
    └── test_user_service.py
```

## Запуск через Docker

### Передумови
- Docker та Docker Compose встановлені на вашій машині.

### Запуск всіх сервісів (додаток + база даних)

```bash
docker-compose up --build
```

Додаток буде доступний за адресою: **http://localhost:5000**

### Зупинка сервісів

```bash
docker-compose down
```

### Зупинка з видаленням даних БД

```bash
docker-compose down -v
```

### Запуск тестів у Docker

```bash
docker-compose run --rm tests
```

## Локальний запуск (без Docker)

### 1. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 2. Запуск додатку

```bash
python app.py
```

Сервер запуститься на `http://localhost:5000`.

### 3. Запуск тестів

```bash
python -m pytest tests/ -v
```

### 4. Запуск лінтерів

```bash
python -m flake8 src/ app.py --max-line-length=120
python -m pylint src/
```

## Змінні середовища

| Змінна | Опис | Значення за замовчуванням |
|--------|------|--------------------------|
| `PORT` | Порт на якому працює додаток | `5000` |
| `FLASK_DEBUG` | Режим дебагу (`0` або `1`) | `0` |
| `DATABASE_URL` | URL підключення до PostgreSQL | не встановлено |
| `POSTGRES_USER` | Ім'я користувача БД (docker-compose) | `store_user` |
| `POSTGRES_PASSWORD` | Пароль користувача БД (docker-compose) | `store_pass` |
| `POSTGRES_DB` | Назва бази даних (docker-compose) | `game_store` |

## API ендпоінти

### Користувачі

| Метод | URL | Опис |
|-------|-----|------|
| `POST` | `/users` | Реєстрація нового користувача |
| `GET` | `/users/<id>` | Отримати дані користувача |

**POST /users — приклад запиту:**
```json
{"user_id": 1, "email": "player@mail.com", "age": 25}
```

**Відповідь (201):**
```json
{"user_id": 1, "email": "player@mail.com", "age": 25, "library": [], "wishlist": []}
```

### Каталог ігор

| Метод | URL | Опис |
|-------|-----|------|
| `GET` | `/games` | Список всіх ігор |
| `GET` | `/games?q=witcher` | Пошук ігор за назвою |
| `GET` | `/games/<id>` | Отримати гру за ID |

**GET /games — приклад відповіді:**
```json
[
  {"game_id": 1, "title": "The Witcher 3"},
  {"game_id": 2, "title": "Cyberpunk 2077"},
  {"game_id": 3, "title": "Minecraft"},
  {"game_id": 4, "title": "The Elder Scrolls V: Skyrim"},
  {"game_id": 5, "title": "Portal 2"}
]
```

### Бібліотека користувача

| Метод | URL | Опис |
|-------|-----|------|
| `POST` | `/users/<id>/library` | Додати гру до бібліотеки |
| `DELETE` | `/users/<id>/library/<game_id>` | Повернути гру (refund) |

**POST /users/1/library — приклад запиту:**
```json
{"game_id": 1}
```

### Список бажаного

| Метод | URL | Опис |
|-------|-----|------|
| `POST` | `/users/<id>/wishlist` | Додати гру до вішліста |

**POST /users/1/wishlist — приклад запиту:**
```json
{"game_id": 2}
```

### Відгуки

| Метод | URL | Опис |
|-------|-----|------|
| `POST` | `/users/<id>/reviews` | Залишити відгук на гру |
| `GET` | `/reviews` | Список усіх відгуків |
| `GET` | `/reviews?game_id=1` | Відгуки для конкретної гри |

**POST /users/1/reviews — приклад запиту:**
```json
{"game_id": 1, "rating": 9, "text": "Masterpiece!"}
```

## Тести

Проєкт містить **39 юніт-тестів** з використанням `pytest` та параметризації:

| Тест-файл | Що перевіряє |
|------------|--------------|
| `test_user_service.py` | Реєстрація: валідація віку (13+), унікальність email |
| `test_store_service.py` | Пошук ігор, покупка, дублікати, вішліст, refund, відгуки (рейтинг 1-10), контроль доступу |

### Запуск тестів та очікуваний результат

```bash
python -m pytest tests/ -v
```

```text
tests/test_store_service.py::test_search_games[Witcher-1] PASSED
tests/test_store_service.py::test_search_games[witcher-1] PASSED
...
tests/test_user_service.py::test_registration_email_uniqueness[a@b.c-d@e.f-False] PASSED

================================= 39 passed in 0.03s =================================
```

## CI/CD конвеєр

Проєкт використовує **GitHub Actions** (`.github/workflows/ci.yml`) з трьома етапами:

1. **Lint** — статичний аналіз коду через `flake8` та `pylint`
2. **Test** — запуск 39 юніт-тестів через `pytest`
3. **Docker** — збірка Docker-образу додатку та запуск тестів у контейнері

Конвеєр запускається автоматично при push та pull request до гілок `main`/`master`.
