from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class GerarSessao:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @property
    def get_engine(self):
        return self.engine
    
    @property
    def get_sessionlocal(self):
        return self.sessionlocal

    def get_db(self):
        db = self.sessionlocal()
        try:
            yield db
        finally:
            db.close()