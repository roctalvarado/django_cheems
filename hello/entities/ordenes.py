from django.db import connection
from ..enums.action import OrderAction

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
                ORDER BY id DESC
            """)                         
            rows = cursor.fetchall()

        return [Ordenes(*row) for row in rows]  

    @staticmethod
    def create(title, description, status, id_user):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO `work_order` 
                    (title, description, status)
                VALUES (%s, %s, %s)
            """, [title, description, status])
            id_work_order = cursor.lastrowid

            cursor.execute("""
                INSERT INTO `work_order_history` (date, id_user, action, id_work_order)
                VALUES (NOW(), %s, %s, %s)
            """, [id_user, OrderAction.CREATED.value , id_work_order])