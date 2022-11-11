from argon2 import PasswordHasher

from db.models import User


class TestUtils:

    @staticmethod
    def add_user_to_in_mem_db(user: User, session):
        ph = PasswordHasher()
        hashed_pw = ph.hash(user.password)
        user.password = hashed_pw
        session.add(user)
        session.commit()
