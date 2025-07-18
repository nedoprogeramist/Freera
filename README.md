1. Установите все зависимости из файла requirements.txt
2. Запустите PostgreSQL 
3. Подключитесь к базе данных командой 
	   psql -U username -d database_name
4. Запустите .sql файл командой 
	   i CreateTable.sql
5. Запустите приложение командой
	uvicorn main:app --reload

