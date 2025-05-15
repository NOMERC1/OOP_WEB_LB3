from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    name: str
    text: Optional[str] = None
    is_done: bool = False

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None
    is_done: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    deleted_at: Optional[str] = None
    class Config:
        from_attributes = True

class TodoListBase(BaseModel):
    name: str

class TodoListCreate(TodoListBase):
    pass

class TodoListUpdate(BaseModel):
    name: Optional[str] = None

class TodoListResponse(TodoListBase):
    id: int
    items: List[ItemResponse] = []
    progress: Optional[float] = None
    deleted_at: Optional[str] = None
    class Config:
        from_attributes = True