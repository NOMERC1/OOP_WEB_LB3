from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime
from src import models, schemas

async def get_todo_lists(db: AsyncSession):
    result = await db.execute(
        select(models.TodoList).where(models.TodoList.deleted_at.is_(None)).order_by(models.TodoList.id)
    )
    return result.scalars().all()

async def create_todo_list(db: AsyncSession, todo: schemas.TodoListCreate):
    db_todo = models.TodoList(name=todo.name)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def update_todo_list(db: AsyncSession, todo_id: int, todo: schemas.TodoListUpdate):
    result = await db.execute(
        select(models.TodoList).where(models.TodoList.id == todo_id, models.TodoList.deleted_at.is_(None))
    )
    db_todo = result.scalar_one_or_none()
    if db_todo:
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        await db.commit()
        await db.refresh(db_todo)
    return db_todo

async def delete_todo_list(db: AsyncSession, todo_id: int):
    result = await db.execute(
        select(models.TodoList).where(models.TodoList.id == todo_id, models.TodoList.deleted_at.is_(None))
    )
    db_todo = result.scalar_one_or_none()
    if db_todo:
        db_todo.deleted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_todo)
    return db_todo

async def get_items(db: AsyncSession, todo_list_id: int):
    result = await db.execute(
        select(models.Item).where(
            models.Item.todo_list_id == todo_list_id,
            models.Item.deleted_at.is_(None)
        )
    )
    return result.scalars().all()

def _update_todo_list_counts(db, todo_list_id):
    # Вспомогательная функция для обновления счетчиков
    async def _inner():
        result = await db.execute(
            select(models.Item).where(
                models.Item.todo_list_id == todo_list_id,
                models.Item.deleted_at.is_(None)
            )
        )
        items = result.scalars().all()
        completed_count = sum(1 for item in items if item.is_done)
        total_count = len(items)
        result = await db.execute(
            select(models.TodoList).where(models.TodoList.id == todo_list_id)
        )
        db_todo = result.scalar_one_or_none()
        if db_todo:
            db_todo.completed_count = completed_count
            db_todo.total_count = total_count
            await db.commit()
            await db.refresh(db_todo)
    return _inner

async def create_item(db: AsyncSession, item: schemas.ItemCreate, todo_list_id: int):
    db_item = models.Item(**item.dict(), todo_list_id=todo_list_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    await _update_todo_list_counts(db, todo_list_id)()
    return db_item

async def update_item(db: AsyncSession, item_id: int, item: schemas.ItemUpdate):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id, models.Item.deleted_at.is_(None))
    )
    db_item = result.scalar_one_or_none()
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)
        await _update_todo_list_counts(db, db_item.todo_list_id)()
    return db_item

async def delete_item(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id, models.Item.deleted_at.is_(None))
    )
    db_item = result.scalar_one_or_none()
    if db_item:
        db_item.deleted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_item)
        await _update_todo_list_counts(db, db_item.todo_list_id)()
    return db_item

async def get_todo_list_by_id(db: AsyncSession, todo_id: int):
    result = await db.execute(
        select(models.TodoList).where(models.TodoList.id == todo_id, models.TodoList.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()

async def get_item_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id, models.Item.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()