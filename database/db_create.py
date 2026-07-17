import psycopg2


def create_tables(connection, cursor):
    create_table_positions = '''
    CREATE TABLE IF NOT EXISTS positions(
    "id" int NOT NULL,
    "должность" varchar NOT NULL, 
    "зарплата" int NOT NULL, 
    CONSTRAINT positions_pk PRIMARY KEY ("id")
    )
    '''

    create_table_division = '''
    CREATE TABLE IF NOT EXISTS division(
    "id" int NOT NULL,
    "подразделение" varchar NOT NULL, 
    CONSTRAINT division_pk PRIMARY KEY ("id")
    )
    '''

    create_table_stuff = '''
    CREATE TABLE IF NOT EXISTS stuff (
    "паспорт" int NOT NULL, 
    "фамилия" varchar NOT NULL,
    "имя" varchar NOT NULL, 
    "отчество" varchar, 
    "подразделение" int NOT NULL, 
    "должность" int NOT NULL, 
    CONSTRAINT stuff_pk PRIMARY KEY ("паспорт"), 
    CONSTRAINT fk1_stuff FOREIGN KEY ("должность") REFERENCES positions("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk2_stuff FOREIGN KEY ("подразделение") REFERENCES division("id") ON DELETE CASCADE ON UPDATE CASCADE 
    )
    '''

    create_table_status = '''
    CREATE TABLE IF NOT EXISTS status (
    "id" int NOT NULL,
    "статус" varchar NOT NULL, 
    CONSTRAINT status_pk PRIMARY KEY ("id")
    )
    '''

    create_table_application = '''
    CREATE TABLE IF NOT EXISTS application (
        "номер заявки" int NOT NULL, 
        "дата создания" date NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        "срок выполнения" int NOT NULL, 
        "автор" int NOT NULL,
        "исполнитель" int,
        "описание" text NOT NULL,
        "статус" int NOT NULL DEFAULT 1,
        CONSTRAINT app_pk PRIMARY KEY ("номер заявки"), 
        CONSTRAINT fk1_app FOREIGN KEY ("автор") REFERENCES stuff("паспорт") ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk2_app FOREIGN KEY ("исполнитель") REFERENCES stuff("паспорт") ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk3_app FOREIGN KEY ("статус") REFERENCES status("id") ON DELETE CASCADE ON UPDATE CASCADE
    )
    '''
    cursor.execute(create_table_positions)
    cursor.execute(create_table_division)
    cursor.execute(create_table_stuff)

    cursor.execute(create_table_status)
    cursor.execute(create_table_application)

    cursor.execute("""
            INSERT INTO division ("id", "подразделение") VALUES 
            (1, 'IT отдел'),
            (2, 'HR отдел'),
            (3, 'Бухгалтерия'),
            (4, 'Отдел продаж'),
            (5, 'Маркетинг')
            ON CONFLICT ("id") DO NOTHING
    """)
    cursor.execute("""
            INSERT INTO positions ("id", "должность", "зарплата") VALUES 
            (1, 'Разработчик', 100000),
            (2, 'Тестировщик', 80000),
            (3, 'Менеджер', 120000),
            (4, 'Аналитик', 110000),
            (5, 'Дизайнер', 90000)
            ON CONFLICT ("id") DO NOTHING
    """)

    cursor.execute("""
            INSERT INTO status ("id", "статус") VALUES 
            (1, 'Новая'), 
            (2, 'В работе'), 
            (3, 'Выполнена')
            ON CONFLICT ("id") DO NOTHING
    """)

    # Создание индексов для оптимизации
    create_indexes = '''
            CREATE INDEX IF NOT EXISTS idx_app_executor ON application ("исполнитель");
            CREATE INDEX IF NOT EXISTS idx_app_status ON application ("статус");
            CREATE INDEX IF NOT EXISTS idx_app_deadline ON application (("дата создания" + "срок выполнения"));
    '''
    cursor.execute(create_indexes)


    connection.commit()
