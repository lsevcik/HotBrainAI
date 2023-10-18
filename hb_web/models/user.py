import enum
import bcrypt
from sqlalchemy import Column, Identity, Integer, String, Enum, select
from sqlalchemy.orm import Session
from database import Base, engine


class Role(enum.Enum):
    USER = 1
    ADMIN = 2


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(), primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(60))
    role = Column(Enum(Role))
    first_name = Column(String(50))
    last_name = Column(String(50))

    def __init__(
        self,
        username=None,
        password=None,
        role=Role.USER,
        first_name=None,
        last_name=None,
    ):
        self.username = username
        self.password = password.decode("UTF-8")
        self.role = role
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"<User {self.username!r}>"


def login(username, **kwargs):
    session = Session(engine)
    stmt = select(User).where(User.username == username)
    result = session.execute(stmt)
    user = result.scalar_one()

    if bcrypt.checkpw(
        kwargs["password"].encode("UTF-8"), user.password.encode("UTF-8")
    ):
        return user
    else:
        return False


def create_default_admin():
    session = Session(engine)
    default_admin = User(
        username="admin",
        password=bcrypt.hashpw(b"admin", bcrypt.gensalt()),
        role=Role.ADMIN,
        first_name="Admin",
        last_name="User",
    )
    session.add(default_admin)
    session.commit()