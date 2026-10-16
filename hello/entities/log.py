from django.db import connection
from ..enums.module import Module

class Log:
    def __init__(self, id, date, description, id_user, module, user_name=None):
        self.id = id
        self.date = date
        self.description = description
        self.id_user = id_user
        self.module = Module(module)
        self.user_name = user_name

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id, l.date, l.description, l.id_user, l.module, u.name 
                FROM `log` l
                LEFT JOIN `user` u ON l.id_user = u.id
            """)
            rows = cursor.fetchall()

            return [Log(*row) for row in rows]