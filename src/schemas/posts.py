from pydantic import BaseModel
from typing import List, Optional

class Posts(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]
    image_url: Optional[str] = None

class update_Posts(Posts):
    id: int
