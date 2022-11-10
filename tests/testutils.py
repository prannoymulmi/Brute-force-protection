from argon2 import PasswordHasher

from db.models import User


class TestUtils:

    @staticmethod
    def add_user_to_in_mem_db(password, session, username):
        ph = PasswordHasher()
        hashed_pw = ph.hash(password)
        user = User(username=username, password=hashed_pw, email="test@test")
        session.add(user)
        session.commit()
