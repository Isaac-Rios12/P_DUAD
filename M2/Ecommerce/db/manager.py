from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from .models.base import Base
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            DATABASE_URL = os.getenv("DATABASE_URL")
            cls._instance.engine = create_engine(DATABASE_URL)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
            print("Engine y session manager instanciados")
        return cls._instance
    
    def get_session(self):
        return self.Session()
    
db = DatabaseManager()

    # def execute(self, stmt, with_commit=False):
    #     try:
    #         with self.Session() as session:
    #             result = session.execute(stmt)
    #             if with_commit:
    #                 session.commit()
    #             return result
    #     except SQLAlchemyError as e:
    #         print("Error durante la ejecucion...", e)
    #         raise
