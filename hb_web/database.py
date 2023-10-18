from sqlalchemy import URL, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from tools.config import get_config

config = get_config()

engine = create_engine(
    URL.create(
        "postgresql+psycopg2",
        username=config.get("POSTGRES_USERNAME", "hotbrain"),
        password=config.get("POSTGRES_PASSWORD", "hotbrain"),
        host=config.get("POSTGRES_HOST", "localhost"),
        database=config.get("POSTGRES_DB", "hotbrain"),
    ),
    echo=True,
)


db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models

    Base.metadata.create_all(bind=engine)
    models.user.create_default_admin()