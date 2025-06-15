# Barter Platform API

Платформа для обмена вещами между пользователями. Пользователи могут создавать объявления, искать вещи по категориям и предлагать обмен.

⸻

### Технологии
```
	•	Python 3.8+
	•	Django 4+
	•	Django REST Framework
	•	SQLite
	•	Django Filters
```

### Установка и запуск

1. Клонируйте репозиторий

```bash
   git clone https://github.com/Monge-Bayir/barter-platform.git
   cd barter-platform
```

2. Создайте виртуальное окружение и активируйте его

```bash
  python -m venv venv
  source venv/bin/activate
```

4. Установите зависимости

```bash
  pip install -r requirements.txt
```

5. Выполните миграции

```bash
   python manage.py makemigrations
   python manage.py migrate
```

6. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

7. Запуск сервера

```bash
  python manage.py runserver
```

### Тесты

```bash
python manage.py test
```


### Возможности
```
	•	Регистрация пользователей (через Django admin)
	•	Создание/редактирование/удаление объявлений
	•	Поиск и фильтрация по категории и состоянию
	•	Отправка и обработка предложений обмена
	•	Защита доступа к редактированию и удалению
```
