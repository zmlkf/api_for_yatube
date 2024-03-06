# Yatube API

API для социальной сети Yatube, где пользователи могут делиться своими постами, комментировать их и подписываться на других пользователей.

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/your_username/api_final_yatube.git
```
2. Перейти в директорию проекта
```bash
cd api_final_yatube
```
3. Установить и активировать виртуальное окружение

```bash
python -m venv venv
```
```bash
source venv/bin/activate
```
```bash
python -m pip install --upgrade pip
```
4. Установить зависимости
```bash
pip install -r requirements.txt
```
5. Перейти в директорию приложения
```bash
cd yatube_api
```
6. Выполнить миграции
```bash
python manage.py migrate
```
7. Запустить сервер
```bash
python manage.py runserver
```
**После выполнения этих шагов, API будет доступно по адресу http://127.0.0.1:8000/**

# Ресурсы API
```bash
http://127.0.0.1:8000/redoc/ - Содержит документацию для API Yatube. В документации описано, как должен работаь API. Документация представлена в формате Redoc.
```
# Формат данных
### API возвращает данные в формате JSON.

Пример успешного ответа:

```bash
{
    "username": "user123",
    "email": "user123@example.com"
}
```
## Автор
Автор: Roman Zemliakov

Email: zemliakovroman97@gmail.com



Этот `readme.md` предоставляет информацию о установке, использовании и ресурсах API, а также примеры запросов и формата данных. Вы можете дополнить его информацией о других функциях и настройках вашего API.