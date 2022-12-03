from fastapi import FastAPI

from web.database import Database
from web.db_service import DbService
from web.settings import APISettings
from web.user_service import get_password_hash

app = FastAPI()
settings = APISettings()
database = Database()
db_service = DbService(settings, database)

# db_service.add_user('admin', get_password_hash('admin'))
db_service.add_strategy('test', open('strategies/example.py', encoding='utf8').read())