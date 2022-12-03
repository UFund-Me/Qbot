from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from web.db_service import DbService

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

route_data = [
    {
        "id": 22,
        "parentId": 2,
        "name": 'ProjectImport',
        "path": '/Project/ProjectImport',
        "component": 'ProjectImport',
        "meta": {"title": '项目导入', "icon": 'el-icon-help'}
    },
    {
        "id": 3,
        "parentId": 0,
        "name": 'Nav',
        "path": '/Nav',
        "component": 'Layout',
        "redirect": '/Nav/SecondNav/ThirdNav',
        "meta": {"title": '多级导航', "icon": 'el-icon-picture'}
    },
    {
        "id": 30,
        "parentId": 3,
        "name": 'SecondNav',
        "path": '/Nav/SecondNav',
        "redirect": '/Nav/SecondNav/ThirdNav',
        "component": 'SecondNav',
        "meta": {"title": '二级导航', "icon": 'el-icon-camera', "alwaysShow": True}
    }
]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserModel(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    roles: List[str] = None


class UserInDB(UserModel):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def get_user(self, username: str):
        return self.db_service.get_user(username)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
