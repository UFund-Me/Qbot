import intercept as intercept
from pydantic import BaseModel


class TaskDTO(BaseModel):
    taskId: str
    serverPath: str
    storagePath: str
    host: str
    port: int
    user: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class StrategyModel(BaseModel):
    name: str
    code: str


class BackTestRequest(BaseModel):
    strategy_id: int
    start_date: float
    end_date: str
    bar_type: str


class BuyRequest(BaseModel):
    security: str
    price: float
    amount: int = 0
    volume: int = 0
    entrust_prop: int = 0


class SellRequest(BaseModel):
    security: str
    price: float
    amount: int = 0
    volume: int = 0
    entrust_prop: int = 0
