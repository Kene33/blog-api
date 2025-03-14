from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str = Field(title="Имя")
    reg_date: str = Field(title="Дата регистрации")
    posts_quantity: int = Field(title="Количество постов")


class UserLoginSchema(BaseModel):
    username: str
    password: str
