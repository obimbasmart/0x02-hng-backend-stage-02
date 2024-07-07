import pytest
from app import main
from app.schemas import UserInCreate, UserOut, UserIn, OrgIn
from app.crude import create_user, create_org
from app.database import Base, engine, get_db

_userInCreate = UserInCreate(firstName="oleg", lastName="bionic",
                             email="oleg@gmail.com", phone="0911234567",
                             password="not_strong_pwd"
    )

_orgInCreate = OrgIn(name="MSFT.org", description="Nice place")


@pytest.fixture
def db_user():
    return create_user(_userInCreate, next(get_db()))

@pytest.fixture
def db_org():
    return create_org(_orgInCreate, next(get_db()))


@pytest.fixture
def user_data_create():
    return _userInCreate

@pytest.fixture
def user_data_login():
    return UserIn(
        email="oleg@gmail.com",
        password="not_strong_pwd"
    )




@pytest.fixture
def access_token():
    response = main.client.post('/auth/login', json=_userInCreate.model_dump())
    return response.json()['data']['accessToken']

@pytest.fixture
def user_data_out():
    return UserOut(
        id = "uuid",
        firstName="oleg",
        lastName="bionic",
        email="oleg@gmail.com",
        phone="0911234567",
    )

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def reset_db():
    reset_database()

@pytest.fixture
def test_client():
    return main.client