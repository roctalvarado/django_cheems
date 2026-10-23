from django.db import connection, transaction
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
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO `work_order` (title, description, status)
                    VALUES (%s, %s, %s)
                """, [title, description, status])
                id_work_order = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO `work_order_history` (date, id_user, action, id_work_order, status)
                    VALUES (NOW(), %s, %s, %s, %s)
                """, [id_user, OrderAction.CREATED.value, id_work_order, status])

    @staticmethod
    def change_status(id_work_order, new_status, id_user):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT status FROM `work_order` WHERE id = %s FOR UPDATE",
                    [id_work_order]
                )
                row = cursor.fetchone()

                if row is None or row[0] == new_status:
                    return False

                cursor.execute(
                    "UPDATE `work_order` SET status = %s WHERE id = %s",
                    [new_status, id_work_order]
                )
                cursor.execute("""
                    INSERT INTO `work_order_history` (date, id_user, action, id_work_order, status)
                    VALUES (NOW(), %s, %s, %s, %s)
                """, [id_user, OrderAction.STATUS_CHANGED.value, id_work_order, new_status])

        return True
