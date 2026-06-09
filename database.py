from sqlmodel import create_engine, SQLModel, Session

# This creates a local file named database.db
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    # This command creates the tables based on your models
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session