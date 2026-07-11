from database import db_config, db_create

connection = db_config.get_connection()
cursor = db_config.get_cursor(connection)

try:
    db_create.create_tables(connection, cursor)

except Exception as e:
    print(f"Ошибка подключения: {e}")
