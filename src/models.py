from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime

class TodoList(Base):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    items = relationship("Item", back_populates="todo_list", cascade="all, delete")
    completed_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    deleted_at = Column(DateTime, nullable=True)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)
    todo_list_id = Column(Integer, ForeignKey("todo_lists.id", ondelete="CASCADE"))
    todo_list = relationship("TodoList", back_populates="items")
    deleted_at = Column(DateTime, nullable=True)