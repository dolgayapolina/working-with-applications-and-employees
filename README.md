# Система управления заявками сотрудников с возможностью фильтрации и составления отчетности

## Содержание
- [Требования](#требования)
- [Установка и настройка](#установка-и-настройка)
- [Запуск программы](#запуск-программы)
- [Структура проекта](#структура-проекта)
- [Функциональность](#функциональность)


## Требования
- Python 3.8 или выше
- PostgreSQL 12 или выше
- Операционная система Windows / macOS / Linux

## Установка и настройка
### 1. Установка PostgreSQL
#### Windows
1. Скачайте установщик с [postgresql.org](https://www.postgresql.org/download/windows/)
2. Запустите установку, запомните пароль пользователя `postgres`
3. Порт по умолчанию: `5432`

#### macOS (через Homebrew)
```bash
brew install postgresql
brew services start postgresql
```

#### Linux
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Создание базы данных
Подключитесь к PostgreSQL и создайте базу данных
```bash
psql -U postgres -h localhost
```
```sql
CREATE DATABASE request_db;
\q
```

### 3. Настройка пользователя
```sql
CREATE USER polina WITH PASSWORD 'your_password';
ALTER DATABASE request_db OWNER TO polina;
GRANT ALL PRIVILEGES ON DATABASE request_db TO polina;
```

### 4. Откройте файл **_database/db_config.py_** и укажите в нем параметры подключения
```python
def get_connection():
    return psycopg2.connect(
        host="localhost",      # Хост
        port="5432",           # Порт
        database="request_db", # Название базы данных
        user="polina",         # Имя пользователя
        password=""            # Пароль
    )
```

### 5. Установка зависимостей
```bash
# Создание виртуального окружения
python -m venv venv

# Активация (macOS/Linux)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

## Запуск программы
Запуск программы происходит путем запуска main.py
```bash
python main.py
```


## Структура проекта
```
Тестовое задание птмк/
├── database/                      # Слой работы с БД
│   ├── db_config.py              # Подключение к PostgreSQL
│   └── db_create.py              # Создание таблиц и индексов
├── models/                       
│   ├── Application.py            # Класс заявки 
│   ├── Stuff.py                  # Класс сотрудника
│   ├── Status.py                 # Класс статуса
│   ├── Devision.py               # Класс подразделения
│   └── Positions.py              # Класс должности
├── repository/                   
│   ├── ApplicationRepository.py  # Работа с заявками в БД
│   └── StuffRepository.py        # Работа с сотрудниками в БД
├── services/                      
│   ├── ApplicationService.py     # Бизнес-логика заявок
│   └── StuffService.py           # Бизнес-логика сотрудников
├── data_generation.py            # Генерация тестовых данных
├── main.py                       # Главный файл
└── requirements.txt              # Зависимости
```

## Функциональность
### Работа с сотрудниками
- Создание сотрудника
- Поиск по паспорту 
- Обновление данных 
- Удаление с проверкой заявок

### Работа с заявками 
- Создание заявки 
- Назначение исполнителя 
- Изменение статуса с проверкой правил 
- Фильтрация по статусу 
- Фильтрация по исполнителю 
- Фильтрация по подразделению 
- Фильтрация по просроченным

### Отчеты
- Количество заявок по статусам
- Количество просроченных заявок
- Количество выполненных заявок по исполнителям

## Автор
Полина Долгая – dolgayapolina

