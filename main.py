import time
from datetime import datetime, timedelta

from database import db_config, db_create
from repository.StuffRepository import StuffRepository
from repository.ApplicationRepository import ApplicationRepository
from services.StuffService import StuffService
from services.ApplicationService import ApplicationService
from data_generation import generate_test_data

from models.Stuff import Stuff
from models.Application import Application


def main():
    connection = db_config.get_connection()
    cursor = db_config.get_cursor(connection)

    try:
        db_create.create_tables(connection, cursor)

        stuff_repo = StuffRepository(connection)
        app_repo = ApplicationRepository(connection)

        app_service = ApplicationService(app_repo)

        # generate_test_data(stuff_repo, app_repo)

        test_stuff = stuff_repo.readStuff(999999)

        test_app = app_repo.readApplication(9999999)

        # Создаем или получаем исполнителя
        executor = stuff_repo.readStuff(888888)

        try:
            # Сначала проверяем, есть ли исполнитель
            if test_app.executor is None:
                print("\nНазначение исполнителя")
                app_service.assign_executor(test_app.id, executor)

            # Переводим в статус "В работе" (если не выполнена)
            if test_app.status == 1:
                print("\nПеревод в статус 'В работе'")
                app_service.complete_application(test_app.id)

            if test_app.status == 2:
                print("\nПеревод в статус 'Выполнена'")
                app_service.complete_application(test_app.id)

        except ValueError as e:
            print(f"Ошибка: {e}")

        print("Фильтрация заявок")

        # По статусу
        print("Заявки в работе:")
        in_progress = app_repo.filterByStatus(2)
        print(f"Найдено: {len(in_progress)} заявок")
        print()

        # По исполнителю
        print("Заявки по исполнителю (паспорт=999999):")
        executor_obj = Stuff(pasport=999999, surname="", name="", patronymic="", division=None, position=None)
        by_executor = app_repo.filterByExecutor(executor_obj.pasport)
        print(f"Найдено: {len(by_executor)} заявок")
        print()

        # По подразделению
        print("Заявки по подразделению IT отдел:")
        by_division = app_repo.filterByDivision(1)
        print(f"Найдено: {len(by_division)} заявок")
        print()

        # По просроченным
        print("Просроченные заявки:")
        overdue = app_repo.filterByOverdue()
        print(f"Найдено: {len(overdue)} просроченных заявок")
        print()

        print("Выполнение запроса")
        print(
            "Вывести все просроченные заявки конкретного исполнителя, находящиеся в статусе «В работе», отсортированные по сроку выполнения")

        executor_pasport = 888888

        print(f"Исполнитель: паспорт {888888}")
        start = time.time()
        final_result = app_repo.finalView(executor_pasport)
        result_time = time.time() - start
        for one_app in final_result:
            print(f"Заявка номер {one_app.id} сорк выполнения {one_app.term}")
        print(len(final_result))
        print(f"Время выполнения запроса с оптимизацией: {result_time}")

        print()
        print("Отчеты")
        print()

        print("Количество заявок по статусам:")
        for i in [(1, "Новая"), (2, "В работе"), (3, "Выполнена")]:
            apps = app_repo.filterByStatus(i[0])
            print(f"Найдено: {len(apps)} заявок в статусе {i[1]}")
        print()

        # Количество просроченных
        print("Количество просроченных заявок:")
        overdue_count = app_repo.filterByOverdue()
        print(f"Всего просроченных: {len(overdue_count)}")
        print()

        executos = stuff_repo.allStuff()
        for pasport in executos:
            apps = app_repo.filterByExecutor(pasport)
            print(f"Найдено {len(apps)} заявок у сотрудника с паспортом {pasport}")


    except Exception as e:
        print(f"{e}")
        import traceback
        traceback.print_exc()

    finally:
        cursor.close()
        db_config.close_connection(connection)


if __name__ == "__main__":
    main()
