from argon2 import PasswordHasher

from db.models import Staff


class TestUtils:

    @staticmethod
    def add_user_to_in_mem_db(user: Staff, session):
        ph = PasswordHasher()
        hashed_pw = ph.hash(user.password)
        user.password = hashed_pw
        session.add(user)
        session.commit()
