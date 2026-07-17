# логика работы с заявками в базе данных
# создание, чтение, обновление, удаление
from database import db_config
from models.Application import Application
from models.Stuff import Stuff


class ApplicationRepository:

    def __init__(self, connection):
        self.conn = connection

    def _rows_to_list(self, rows):
        apps = []
        for row in rows:
            author = Stuff(
                pasport=row[3],
                surname="",
                name="",
                patronymic="",
                division=None,
                position=None
            )

            executor = None
            if row[4]:
                executor = Stuff(
                    pasport=row[4],
                    surname="",
                    name="",
                    patronymic="",
                    division=None,
                    position=None
                )

            apps.append(Application(
                id=row[0],
                date=row[1],
                term=row[2],
                author=author,
                executor=executor,
                status=row[6],
                description=row[5]
            ))
        return apps

    def createApplication(self, application):  # application - объект класса Application
        cursor = db_config.get_cursor(self.conn)

        try:
            if application.author is None:
                raise ValueError("Автор заявки обязателен!")

            create_app = '''
                INSERT INTO application ("номер заявки", "дата создания", "срок выполнения", "автор", "исполнитель", "описание", "статус" )
                 VALUES (%s, %s, %s, %s, %s, %s, %s)
                 ON CONFLICT ("номер заявки") DO NOTHING
            '''
            cursor.execute(create_app, (
                application.id, application.date, application.term, application.author.pasport, application.executor.pasport if application.executor else None,
                application.description, application.status))
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении заявки: {e}")
            raise
        finally:
            cursor.close()

    def readApplication(self, id):
        cursor = db_config.get_cursor(self.conn)

        read_stuff = '''
                    SELECT * FROM application 
                    WHERE "номер заявки" = %s
                '''

        cursor.execute(read_stuff, (id,))

        row = cursor.fetchone()
        if row is None:
            return None

        cursor.close()
        return self._rows_to_list([row])[0]

    def updateApplication(self, application):
        cursor = db_config.get_cursor(self.conn)

        try:
            update_stuff = '''
                        UPDATE application
                        SET "исполнитель"=%s, "описание"=%s, "статус"=%s
                        WHERE "номер заявки"=%s
                    '''

            cursor.execute(update_stuff,
                           (application.executor.pasport, application.description, application.status, application.id))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def deleteApplication(self, id):
        cursor = db_config.get_cursor(self.conn)

        try:
            delete_stuff = '''
                DELETE FROM application WHERE "номер заявки" = %s
            '''
            cursor.execute(delete_stuff, (id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def filterByStatus(self, status_id):
        cursor = db_config.get_cursor(self.conn)

        try:
            select_app = '''
                SELECT * FROM application 
                WHERE "статус" = %s
                ORDER BY "номер заявки"
            '''
            cursor.execute(select_app, (status_id,))
            return self._rows_to_list(cursor.fetchall())

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def filterByExecutor(self, pasport):
        cursor = db_config.get_cursor(self.conn)

        try:
            select_app = '''
                SELECT * FROM application 
                WHERE "исполнитель" = %s
                ORDER BY "номер заявки"
            '''
            cursor.execute(select_app, (pasport,))
            return self._rows_to_list(cursor.fetchall())

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def filterByDivision(self, division):
        cursor = db_config.get_cursor(self.conn)

        try:
            select_app = '''
                SELECT * FROM application 
                JOIN stuff ON application."исполнитель"=stuff."паспорт"
                WHERE stuff."подразделение" = %s
                ORDER BY "номер заявки"
            '''
            cursor.execute(select_app, (division,))
            return self._rows_to_list(cursor.fetchall())

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def filterByOverdue(self):
        cursor = db_config.get_cursor(self.conn)

        try:
            select_app = '''
                SELECT * FROM application 
                WHERE ("дата создания" + "срок выполнения") < CURRENT_DATE
                ORDER BY ("дата создания" + "срок выполнения") ASC
            '''
            cursor.execute(select_app)
            return self._rows_to_list(cursor.fetchall())

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def finalView(self, pasport):
        cursor = db_config.get_cursor(self.conn)

        try:
            select_app = '''
                SELECT * FROM application
                WHERE application."статус" = 2 AND application."исполнитель"=%s
                ORDER BY "срок выполнения" ASC
            '''
            cursor.execute(select_app, (pasport,))
            return self._rows_to_list(cursor.fetchall())

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

