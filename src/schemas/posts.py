from pydantic import BaseModel
from typing import List

class Posts(BaseModel):
    title: str
    content: str
    category: str
    tags: List

class update_Posts(Posts):
    id: int
