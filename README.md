# 1. Создаём виртуальное окружение:
   - python3 -m venv venv
   - source venv/bin/activate

# 2. Устанавливаем библиотеки:
   - pip install -r requirements.txt

# 3. Создаём БД через docker-compose:
   - docker-compose up -d

# 4. Запускаем приложение (номер = id супергероя):
   - python3 main2.py 1


# __for info: BD:
	name db:  asincio_bd
	user:	  postgres
	password: postgres
	port: 5439
