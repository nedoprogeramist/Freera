migrations = [
	 """
	CREATE CREATE DATABASE fastapi-postgres WITH OWNER postgres ENCODING 'UTF8';
	\connect fastapi-postgres;
	CREATE TYPE issuse_status AS ENUM ( 'TODO', 'In Progress', 'Review', 'QA', 'Done', 'Closed' );
	CREATE TABLE IF NOT EXISTS issuse( id int PRIMARY KEY AUTO_INCREMENT, key str, name str, status issuse_status, description str );
	 """
]

