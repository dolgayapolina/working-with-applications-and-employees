import random
from datetime import datetime, timedelta
from models.Stuff import Stuff
from models.Application import Application


def generate_test_data(stuff_repo, app_repo, num_stuff=1000, num_apps=1000000):
    stuff_list = []

    # Добавляем служебных сотрудников для тестов
    test_stuff = Stuff(
        pasport=999999,
        surname="Тестов",
        name="Тест",
        patronymic="Тестович",
        division=1,
        position=1
    )

    stuff_repo.createStuff(test_stuff)
    stuff_list.append(test_stuff)

    executor = Stuff(
        pasport=888888,
        surname="Исполнителев",
        name="Исполнитель",
        patronymic="Исполнителевич",
        division=1,
        position=2
    )
    stuff_repo.createStuff(executor)
    stuff_list.append(executor)

    # Генерируем остальных сотрудников
    for i in range(3, num_stuff + 1):
        pasport = 100000 + i
        stuff = Stuff(
            pasport=pasport,
            surname=f"Фамилия_{i}",
            name=f"Имя_{i}",
            patronymic=f"Отчество_{i}",
            division=random.randint(1, 5),  # 5 подразделений
            position=random.randint(1, 5)  # 5 должностей
        )
        stuff_repo.createStuff(stuff)
        stuff_list.append(stuff)

    # Генерируем заявки
    test_app = Application(
        id=9999999,
        date=datetime.now().date(),
        term=5,
        author=test_stuff,
        executor=None,
        description="Тестовая заявка для демонстрации",
        status=1  # Новая
    )
    app_repo.createApplication(test_app)

    for i in range(1, num_apps + 1):
        if i == 9999999:
            continue

        days_ago = random.randint(0, 365)
        date_created = datetime.now().date() - timedelta(days=days_ago)
        term = random.randint(1, 30)
        author = random.choice(stuff_list)
        executor = random.choice(stuff_list)
        status = random.randint(1, 3)
        description = f"Описание заявки {i}"

        app = Application(
            id=i,
            date=date_created,
            term=term,
            author=author,
            executor=executor,
            description=description,
            status=status
        )
        app_repo.createApplication(app)
