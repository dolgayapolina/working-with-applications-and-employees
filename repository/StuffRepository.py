# логика работы с сотрудниками в базе данных
# создание, чтение, обновление, удаление
from database import db_config
from models.Stuff import Stuff


class StuffRepository:

    def __init__(self, connection):
        self.conn = connection

    def createStuff(self, stuff):  # stuff - объект класса Staff
        cursor = db_config.get_cursor(self.conn)
        try:
            add_stuff = '''
                INSERT INTO stuff ("паспорт", "фамилия", "имя", "отчество", "подразделение", "должность")
                VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT ("паспорт") DO NOTHING
            '''

            cursor.execute(add_stuff,
                           (stuff.pasport, stuff.surname, stuff.name, stuff.patronymic, stuff.division, stuff.position))

            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении сотрудника: {e}")
            raise
        finally:
            cursor.close()

    def readStuff(self, pasport):
        cursor = db_config.get_cursor(self.conn)

        read_stuff = '''
            SELECT * FROM stuff 
            WHERE "паспорт" = %s
        '''

        cursor.execute(read_stuff, (pasport,))

        row = cursor.fetchone()
        if row is None:
            return None

        cursor.close()
        return Stuff(row[0], row[1], row[2], row[3], row[4], row[5])

    def updateStuff(self, stuff):
        cursor = db_config.get_cursor(self.conn)

        try:
            update_stuff = '''
                UPDATE stuff
                SET "фамилия"=%s, "имя"=%s, "отчество"=%s, "подразделение"=%s, "должность"=%s
                WHERE "паспорт"=%s
            '''

            cursor.execute(update_stuff,
                           (stuff.surname, stuff.name, stuff.patronymic, stuff.division, stuff.position, stuff.pasport))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def deleteStuff(self, pasport):
        cursor = db_config.get_cursor(self.conn)

        try:
            delete_stuff = '''
                DELETE FROM stuff WHERE "паспорт" = %s
            '''
            cursor.execute(delete_stuff, (pasport,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
