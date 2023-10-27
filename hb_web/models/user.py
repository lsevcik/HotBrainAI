import enum
import bcrypt
from sqlalchemy import Column, ForeignKey, Identity, Integer, String, Enum, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from database import Base, engine


class Role(enum.Enum):
    USER = 1
    ADMIN = 2


class GenderClass(enum.Enum):
    CISGENDER = 1
    TRANSGENDER = 2
    OTHER = 3


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


class Seeking(enum.Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class UserSeeking(Base):
    __tablename__ = "users_seeking"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    seeking = Column(Enum(Seeking), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(), primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(60))
    role = Column(Enum(Role))
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender_class = Column(Enum(GenderClass))
    gender = Column(Enum(Gender))
    seeking: Mapped[list["UserSeeking"]] = relationship()

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
        return None


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