import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DataProvider():
    def __init__(self):
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user="romablunt",
                                  # пароль, который указали при установке PostgreSQL
                                  password="CGGZ*gZQ2A1K63SV",
                                  host="pg3.sweb.ru",
                                  port="5432")
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            print("Подкючение к PostgreSQL прошло успешно")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        
    def exQuery(self, sqltext: str, vars):
        self.cursor.execute(sqltext,vars)
        if (sqltext.upper().startswith('INSERT')) or (sqltext.upper().startswith('UPDATE')):
            self.connection.commit()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Соединение с PostgreSQL закрыто")