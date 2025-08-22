from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.tasks import TaskCreate, TaskFromDB, TaskUpdate
from fake_db.fake_dao import TasksDAO, get_task_dao

tasks_router = APIRouter(
    prefix="/task",
    tags=["Task"],
)


@tasks_router.post("", response_model=TaskFromDB | dict, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate,
                      task_dao: TasksDAO = Depends(get_task_dao)):
    task_id = uuid4()
    name, description, state = task_data.model_dump().values()

    task_dao.add_one((str(task_id), name, description, state.value))

    return TaskFromDB(
        id=task_id,
        name=name,
        description=description,
        status=state
    )


@tasks_router.get("/{task_id}", response_model=TaskFromDB | dict, status_code=status.HTTP_200_OK)
async def get_task(task_id: str,
                   task_dao: TasksDAO = Depends(get_task_dao)):

    task_from_db = task_dao.get_one("id", task_id)

    if task_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {task_id} not found")
    else:
        return task_from_db


@tasks_router.delete("/{task_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_task(task_id: str,
                      task_dao: TasksDAO = Depends(get_task_dao)):
    task_from_db = task_dao.delete_one("id", task_id)

    if task_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {task_id} not found")
    else:
        return {"detail": f"Task with id {task_id} successfully deleted"}


@tasks_router.put("/{task_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id: str,
                      task_data: TaskUpdate,
                      task_dao: TasksDAO = Depends(get_task_dao)):
    task_from_db = task_dao.update_one("id", task_id, task_data.model_dump())

    if task_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {task_id} not found")
    else:
        return {"detail": f"Task with id {task_id} successfully updated"}


@tasks_router.get("/{offset}/{limit}", response_model=list[TaskFromDB])
async def get_reports_pack(offset: str,
                           limit: str,
                           task_dao: TasksDAO = Depends(get_task_dao),
                           ):
    tasks_list_from_db = task_dao.get_pack(int(offset), int(limit))

    if tasks_list_from_db:
        return tasks_list_from_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task list is empty")
