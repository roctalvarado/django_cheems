from django.db import connection

class Ordenes:
    def __init__(self, id, title, description, status):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
            

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, status
                FROM `work_order`
            """)                         
            rows = cursor.fetchall()

        return [Ordenes(*row) for row in rows]  