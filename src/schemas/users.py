from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str = Field(title="Имя")
    reg_date: str = Field(title="Дата регистрации")
    posts_quantity: int = Field(title="Количество постов")

class UserAdd(User):
    login: str = Field(title="Логин")
    password: str = Field(title="Пароль")

class RegisterRequest(BaseModel):
    name: str = Field(title="Имя")
    createdAt: str = Field(title="Дата регистрации")
    email: str
    username: str
    password: str
    image_url: str

class LoginRequest(BaseModel):
    username: str
    password: str