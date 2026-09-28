from pydantic import BaseModel

class RouteRequest(BaseModel):
    origin: str
    destination: str
    cargo_type: str
    containers: int


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str