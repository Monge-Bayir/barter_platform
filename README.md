Barter Platform API

Платформа для обмена вещами между пользователями. Пользователи могут создавать объявления, искать вещи по категориям и предлагать обмен.

⸻

Технологии
	•	Python 3.8+
	•	Django 4+
	•	Django REST Framework
	•	SQLite
	•	Django Filters


Установка и запуск

1. Клонируйте репозиторий
   git clone https://github.com/Monge-Bayir/barter-platform.git
   cd barter-platform

2. Создайте виртуальное окружение и активируйте его
  python -m venv venv
  source venv/bin/activate

3. Установите зависимости
  pip install -r requirements.txt

4. Выполните миграции
   python manage.py makemigrations
   python manage.py migrate
   
5. Создайте суперпользователя
  python manage.py createsuperuser

6. Запуск сервера
  python manage.py runserver


Тесты
python manage.py test


Возможности
	•	Регистрация пользователей (через Django admin)
	•	Создание/редактирование/удаление объявлений
	•	Поиск и фильтрация по категории и состоянию
	•	Отправка и обработка предложений обмена
	•	Защита доступа к редактированию и удалению
