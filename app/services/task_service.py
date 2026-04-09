from sqlalchemy.orm import Session
from app.models.task_model import Task
from fastapi import HTTPException
from app.enum_fdr.status_enum import Status
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exception_handler import handle_db_error
from app.models.user_model import User



def create_task_service(db, task, current_user, employee_id):
    try:
        # ✅ Get employee
        employee = db.query(User).filter(User.id == employee_id).first()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # 🔐 ROLE BASED VALIDATION

        # ✅ SUPER ADMIN (FULL ACCESS)
        if current_user["role"] == "super_admin":
            mnc_id = employee.mnc_id
            org_id = employee.organization_id

        # ✅ MNC ADMIN
        elif current_user["role"] == "mnc_admin":
            if employee.mnc_id != current_user["mnc_id"]:
                raise HTTPException(403, "Not your MNC")

            mnc_id = employee.mnc_id
            org_id = employee.organization_id

        # ✅ ORG ADMIN
        elif current_user["role"] == "org_admin":
            if employee.organization_id != current_user["organization_id"]:
                raise HTTPException(403, "Not your organization")

            mnc_id = None
            org_id = employee.organization_id

        # ❌ EMPLOYEE
        else:
            raise HTTPException(403, "Employees cannot assign tasks")

        # ✅ CREATE TASK
        new_task = Task(
            title=task.title,
            description=task.description,
            assigned_by=current_user["role"],
            assigned_to=employee.name,
            status=task.status.value,
            employee_id=employee.id,
            mnc_id=mnc_id,
            organization_id=org_id
        )

        # print("CURRENT USER:", current_user)
        # print("EMPLOYEE:", employee.id, employee.mnc_id, employee.organization_id)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except SQLAlchemyError as e:
        handle_db_error(db, e)






def get_task_by_scope(db, current_user):

    if current_user["role"] == "super_admin":
        return db.query(Task).all()

    elif current_user["role"] == "mnc_admin":
        return db.query(Task).filter(
            Task.mnc_id == current_user["mnc_id"]
        ).all()

    elif current_user["role"] == "org_admin":
        return db.query(Task).filter(
            Task.organization_id == current_user["organization_id"]
        ).all()

    else:
        return db.query(Task).filter(
            Task.employee_id == current_user["id"]
        ).all()


def get_all_task(db:Session):
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task




def update_task(db:Session,task_id:int,title:str,description:str,assigned_by:str,assigned_to:str,status:Status,current_user):
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found with this id")
    
    
    task.title=title
    task.description=description
    task.assigned_by=assigned_by
    task.assigned_to=assigned_to
    task.status=status.value

    db.commit()
    db.refresh(task)
    
    return task




def delete_task(db:Session,task_id:int):
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found with this id")
    
    
    db.delete(task)
    db.commit()
    
    
    return {"Message":"Task deleted succesfully"}







def update_task_status(db, task_id, status, current_user):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # ✅ VALIDATE STATUS (STRING OR ENUM BOTH SUPPORT)
    valid_status = ["pending", "in_progress", "completed"]

    if hasattr(status, "value"):  # enum case
        status_value = status.value
    
    elif status_value not in valid_status:
        raise HTTPException(
            # status_code=400,
            detail="Status must be 'pending', 'in_progress' or 'completed'"
        )
        
    else:
        status_value = status

        

    if current_user["role"] == "super_admin":
        pass

    # ✅ MNC ADMIN (can update any task in same MNC)
    elif current_user["role"] == "mnc_admin":
        if task.mnc_id != current_user["mnc_id"]:
            raise HTTPException(403, "Not your MNC")

    # ✅ ORG ADMIN
    elif current_user["role"] == "org_admin":
        if task.organization_id != current_user["organization_id"]:
            raise HTTPException(403, "Not your organization")

    # ✅ EMPLOYEE
    elif current_user["role"] == "employee":
        if task.employee_id != current_user["id"]:
            raise HTTPException(403, "You can only update your own task")

    task.status = status.value

    db.commit()
    db.refresh(task)

    return {"Message":"Task updated","Task":task.status}