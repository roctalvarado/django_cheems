from django.db import connection
from ..enums.action import OrderAction
from ..enums.status import Status


class OrderHistory:
    def __init__(self, id, date, id_user, action, id_work_order, title=None, status=None):
        self.id = id
        self.date = date
        self.id_user = id_user
        self.action = OrderAction(action).name if action is not None else '-'
        self.id_work_order = id_work_order
        self.title = title
        self.status = Status(status).name if status is not None else '-'
            

    @staticmethod
    def get_by_user(id_user):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT h.id, h.date, h.id_user, h.action, h.id_work_order,
                       w.title, w.status
                FROM `work_order_history` h
                LEFT JOIN `work_order` w ON h.id_work_order = w.id
                WHERE h.id_user = %s
                ORDER BY h.date DESC, h.id DESC
            """, [id_user])
            rows = cursor.fetchall()

        return [OrderHistory(*row) for row in rows]