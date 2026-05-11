from fastapi import APIRouter, status, HTTPException, Depends

from app.api.dependencies import get_task_service
from app.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from app.services.task import TaskService, TaskNotFound

router = APIRouter(prefix="/tasks")

@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
        payload: TaskCreateSchema,
        task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.create_task(task_create=payload)


@router.patch("/{task_id}")
def update_task(
        task_id: str,
        payload: TaskUpdateSchema,
        task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: str,
        task_service: TaskService = Depends(get_task_service),
) -> None:
    try:
        task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
'''
категории в другой роутер


@app.get("/categories")
def read_categories() -> list[CategorySchema]:
    rows = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(c) for c in rows]
 

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, ) -> CategorySchema:
    category = CategoryORM(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category_orm_to_model(category)



@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoryUpdateSchema, ) -> CategorySchema:
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if payload.name is not None:
        category.name = payload.name
    db.commit()
    db.refresh(category)
    return category_orm_to_model(category)


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, ) -> None:
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
'''