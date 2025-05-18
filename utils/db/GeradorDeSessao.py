from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

class GerarSessao:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url)
        self.sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @property
    def get_engine(self) -> Engine:
        return self.engine
    
    @property
    def get_sessionlocal(self) -> sessionmaker[Session]:
        return self.sessionlocal

    def get_db(self) -> Generator[Session, None, None]:
        db = self.sessionlocal()
        try:
            yield db
        finally:
            db.close()