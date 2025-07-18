Создание типа данных для сохранения статуса
========================================

CREATE TYPE IF NOT EXISTS issue_status AS ENUM ( 'TODO', 'In Progress', 'Review', 'QA', 'Done', 'Closed' );

========================================

Создание таблицы
========================================

CREATE TABLE IF NOT EXISTS issue( id int PRIMARY KEY AUTO_INCREMENT, key str, name str, status issue_status, description str );

========================================
