from django.db import connection
from django.contrib.auth.hashers import make_password, check_password, identify_hasher
from django.utils.crypto import constant_time_compare
from ..enums.profile import Profile

class User:
    def __init__(self, name, account, profile):
        self.name = name
        self.account = account
        self.profile = Profile(profile)

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name, account, profile 
                FROM `user`
            """)
            rows = cursor.fetchall()

            return [User(*row) for row in rows]

    @staticmethod
    def create(name, account, password, profile):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO `user` (name, account, password, profile) VALUES (%s, %s, %s, %s)",
                [name, account, make_password(password), int(profile)]
            )

    @staticmethod
    def authenticate(account, password):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, profile, password FROM `user` WHERE account = %s",
                [account]
            )
            row = cursor.fetchone()

        if row is None or not row[3]:
            return None

        stored_password = row[3]

        try:
            identify_hasher(stored_password)
            is_hashed = True
        except ValueError:
            is_hashed = False

        if is_hashed:
            if not check_password(password, stored_password):
                return None
        else:
            # Contraseña vieja sin hashear: se compara directo
            if not constant_time_compare(password, stored_password):
                return None
            # y se guarda hasheada para la próxima vez
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE `user` SET password = %s WHERE id = %s",
                    [make_password(password), row[0]]
                )

        return {'id': row[0], 'name': row[1], 'profile': row[2]}