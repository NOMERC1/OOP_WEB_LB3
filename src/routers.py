from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src import crud, schemas

router = APIRouter()

@router.get("/todos", response_model=list[schemas.TodoListResponse])
async def get_todo_lists(db: AsyncSession = Depends(get_db)):
    todos = await crud.get_todo_lists(db)
    for todo in todos:
        todo.progress = (todo.completed_count / todo.total_count * 100) if todo.total_count else 0.0
    return todos

@router.post("/todos", response_model=schemas.TodoListResponse)
async def create_todo_list(todo: schemas.TodoListCreate, db: AsyncSession = Depends(get_db)):
    todo_obj = await crud.create_todo_list(db, todo)
    todo_obj.progress = (todo_obj.completed_count / todo_obj.total_count * 100) if todo_obj.total_count else 0.0
    return todo_obj

@router.patch("/todos/{todo_id}", response_model=schemas.TodoListResponse)
async def update_todo_list(todo_id: int, todo: schemas.TodoListUpdate, db: AsyncSession = Depends(get_db)):
    updated_todo = await crud.update_todo_list(db, todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="TodoList not found")
    updated_todo.progress = (updated_todo.completed_count / updated_todo.total_count * 100) if updated_todo.total_count else 0.0
    return updated_todo

@router.delete("/todos/{todo_id}", response_model=schemas.TodoListResponse)
async def delete_todo_list(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.delete_todo_list(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="TodoList not found")
    todo.progress = (todo.completed_count / todo.total_count * 100) if todo.total_count else 0.0
    return todo

@router.get("/todos/{todo_id}/items", response_model=list[schemas.ItemResponse])
async def get_items(todo_id: int, db: AsyncSession = Depends(get_db)):
    items = await crud.get_items(db, todo_id)
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items

@router.post("/todos/{todo_id}/items", response_model=schemas.ItemResponse)
async def create_item(todo_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, item, todo_id)

@router.patch("/items/{item_id}", response_model=schemas.ItemResponse)
async def update_item(item_id: int, item: schemas.ItemUpdate, db: AsyncSession = Depends(get_db)):
    updated_item = await crud.update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", response_model=schemas.ItemResponse)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/todos/{todo_id}", response_model=schemas.TodoListResponse)
async def get_todo_list_by_id(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo_list_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="TodoList not found")
    todo.progress = (todo.completed_count / todo.total_count * 100) if todo.total_count else 0.0
    return todo

@router.get("/items/{item_id}", response_model=schemas.ItemResponse)
async def get_item_by_id(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item