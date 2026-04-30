# Lab 5: Business Logic & Refactoring

Реалізація бекенд-частини бізнес-логіки для магазину відеоігор з використанням архітектури Controller-Service-Repository та покриттям юніт-тестами.

##  Архітектура
Проєкт суворо дотримується архітектурного шаблону **Controller-Service-Repository** для забезпечення принципу єдиної відповідальності (SRP) та розділення обов'язків (Separation of Concerns):
- **`models/`**: Класи даних (`@dataclass`), що представляють сутності предметної області (`User`, `Game`, `Review`).
- **`repositories/`**: Шар доступу до даних, відповідальний за збереження, пошук та отримання сутностей (у цій лабораторній роботі імітується зберігання в оперативній пам'яті - in-memory).
- **`services/`**: Ядро бізнес-логіки, валідація даних та забезпечення виконання правил (наприклад, вікові обмеження, автоматичне видалення зі списку бажаного).
- **`controllers/`**: Точки входу API, які обробляють вхідні запити та направляють їх до відповідних сервісів.

##  Структура каталогів
```text
lab5/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── repositories/
│   └── services/
└── tests/
    ├── test_store_service.py
    └── test_user_service.py
```
##  Основний реалізований функціонал
- Реєстрація користувачів: Валідація віку (13+) та перевірка унікальності email.

- Пошукова система: Пошук ігор за назвою (нечутливий до регістру) з можливістю часткового збігу.

- Керування бібліотекою: Симуляція покупки та запобігання дублюванню ігор в акаунті.

- Список бажаного (Wishlist): Автоматичне видалення ігор зі списку бажаного після їх фактичного придбання.

- Система відгуків: Валідація оцінок (від 1 до 10) та строгий контроль доступу (відгуки можуть залишати лише власники ігор).

##  Встановлення та налаштування
Щоб встановити необхідні залежності для розробки та тестування, виконайте наступну команду в терміналі:
```text
pip install pytest pylint
```
##  Запуск тестів
Проєкт включає набір із 39 юніт-тестів, що використовують параметризацію pytest для покриття крайових випадків, граничних значень та очікуваних виключень.

Щоб запустити тести та побачити детальний вивід, виконайте:
```text
python -m pytest tests/ -v
```
##  Результат тестів
```text
collected 39 items                                                                                                                                                                                                       

tests/test_store_service.py::test_search_games[Witcher-1] PASSED                                                                                                                                                   [  2%]
tests/test_store_service.py::test_search_games[witcher-1] PASSED                                                                                                                                                   [  5%]
tests/test_store_service.py::test_search_games[WITCHER-1] PASSED                                                                                                                                                   [  7%]
tests/test_store_service.py::test_search_games[craft-1] PASSED                                                                                                                                                     [ 10%]
tests/test_store_service.py::test_search_games[The-2] PASSED                                                                                                                                                       [ 12%]
tests/test_store_service.py::test_search_games[e-4] PASSED                                                                                                                                                         [ 15%]
tests/test_store_service.py::test_search_games[GTA 6-0] PASSED                                                                                                                                                     [ 17%]
tests/test_store_service.py::test_search_games[-5] PASSED                                                                                                                                                          [ 20%]
tests/test_store_service.py::test_search_games[   -5] PASSED                                                                                                                                                       [ 23%]
tests/test_store_service.py::test_add_game_success PASSED                                                                                                                                                          [ 25%]
tests/test_store_service.py::test_add_game_exceptions[99-1] PASSED                                                                                                                                                 [ 28%]
tests/test_store_service.py::test_add_game_exceptions[1-99] PASSED                                                                                                                                                 [ 30%]
tests/test_store_service.py::test_add_game_exceptions[99-99] PASSED                                                                                                                                                [ 33%]
tests/test_store_service.py::test_add_game_duplicate PASSED                                                                                                                                                        [ 35%]
tests/test_store_service.py::test_wishlist_flow PASSED                                                                                                                                                             [ 38%]
tests/test_store_service.py::test_wishlist_logic[add_to_library] PASSED                                                                                                                                            [ 41%]
tests/test_store_service.py::test_wishlist_logic[add_to_wishlist] PASSED                                                                                                                                           [ 43%]
tests/test_store_service.py::test_refund_success PASSED                                                                                                                                                            [ 46%]
tests/test_store_service.py::test_refund_exceptions[1-2] PASSED                                                                                                                                                    [ 48%]
tests/test_store_service.py::test_refund_exceptions[99-1] PASSED                                                                                                                                                   [ 51%]
tests/test_store_service.py::test_reviews[1-True] PASSED                                                                                                                                                           [ 53%]
tests/test_store_service.py::test_reviews[5-True] PASSED                                                                                                                                                           [ 56%]
tests/test_store_service.py::test_reviews[10-True] PASSED                                                                                                                                                          [ 58%]
tests/test_store_service.py::test_reviews[0-False] PASSED                                                                                                                                                          [ 61%]
tests/test_store_service.py::test_reviews[-1-False] PASSED                                                                                                                                                         [ 64%]
tests/test_store_service.py::test_reviews[11-False] PASSED                                                                                                                                                         [ 66%]
tests/test_store_service.py::test_reviews[99-False] PASSED                                                                                                                                                         [ 69%]
tests/test_store_service.py::test_review_access[2-1] PASSED                                                                                                                                                        [ 71%]
tests/test_store_service.py::test_review_access[1-2] PASSED                                                                                                                                                        [ 74%]
tests/test_user_service.py::test_registration_age_boundaries[13-True] PASSED                                                                                                                                       [ 76%]
tests/test_user_service.py::test_registration_age_boundaries[14-True] PASSED                                                                                                                                       [ 79%]
tests/test_user_service.py::test_registration_age_boundaries[99-True] PASSED                                                                                                                                       [ 82%]
tests/test_user_service.py::test_registration_age_boundaries[12-False] PASSED                                                                                                                                      [ 84%]
tests/test_user_service.py::test_registration_age_boundaries[0-False] PASSED                                                                                                                                       [ 87%]
tests/test_user_service.py::test_registration_age_boundaries[-5-False] PASSED                                                                                                                                      [ 89%]
tests/test_user_service.py::test_registration_email_uniqueness[test@mail.com-test@mail.com-True] PASSED                                                                                                            [ 92%]
tests/test_user_service.py::test_registration_email_uniqueness[user1@mail.com-user2@mail.com-False] PASSED                                                                                                         [ 94%]
tests/test_user_service.py::test_registration_email_uniqueness[ADMIN@mail.com-ADMIN@mail.com-True] PASSED                                                                                                          [ 97%]
tests/test_user_service.py::test_registration_email_uniqueness[a@b.c-d@e.f-False] PASSED                                                                                                                           [100%]

=================================================================================================== 39 passed in 0.03s ==================================================================================================
```

## Якість коду та лінтинг
Кодова база повністю відповідає стандартам PEP 8. 
Щоб запустити лінтер і перевірити оцінку якості коду, виконайте:
```text
python -m pylint src/
```
## Результат pylint
```text
-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 8.90/10, +1.10)
```


