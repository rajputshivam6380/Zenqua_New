from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schema import TaskCreate,TaskResponse,TaskUpdate,TaskStatusUpdate
from app.services import task_service
from app.auth.dependencies import get_current_actor, require_role
from app.enum_fdr.roles import Roles

task_router=APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/assign/{employee_id}", response_model=TaskResponse)
def assign_task(
    employee_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role([
        Roles.SUPER_ADMIN,
        Roles.MNC_ADMIN,
        Roles.ORG_ADMIN
    ]))
):
    return task_service.create_task_service(db, task, user, employee_id)


@task_router.get("/my-tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(get_current_actor)
):
    return task_service.get_task_by_scope(db, user)


@task_router.get("/", response_model=list[TaskResponse])
def get_task(db:Session=Depends(get_db)):
    return task_service.get_all_task(db)





@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id:int,db:Session=Depends(get_db)):
    return task_service.get_task_by_id(db,task_id)



@task_router.put("/{task_id}",response_model=TaskResponse)
def update_org(task_id:int,org:TaskUpdate,db:Session=Depends(get_db)):
    return task_service.update_task(db,task_id,org.title,org.description,org.assigned_by,org.assigned_to,org.status)


@task_router.delete("/{task_id}")
def delete_org(task_id:int,db:Session=Depends(get_db)):
    return task_service.delete_task(db,task_id)







@task_router.patch("/status/{task_id}")
def update_status(
    task_id: int,
    task: TaskStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_actor)
):
    return task_service.update_task_status(db, task_id, task.status, user)