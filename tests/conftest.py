from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from db import models, dbconfig
from main import app
import pytest

"""

Using fixtures to set up in-mem database for a test https://docs.pytest.org/en/6.2.x/fixture.html
The fixtures are set with scope function, which indicates that the session and client can be reused in the all the test in this package. It is also 
is newly recreated for every test so that there are no side effects.
"""


@pytest.fixture(name="session", scope="function", autouse=True)
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    models.SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client", scope="function", autouse=True)
def client_fixture(session: Session):
    def session_scope_override():
        return session  #

    app.dependency_overrides[dbconfig.get_session] = session_scope_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

