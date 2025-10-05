# Libs
from sqlalchemy.orm import sessionmaker
from core.db.connection import get_engine


sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
session = sessionLocal()
