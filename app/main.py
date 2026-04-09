from fastapi import FastAPI
from app.database import engine, Base

from app.routes.auth_routes import auth_router
from app.routes.admin_routes import admin_router
from app.routes.employee_routes import employee_router
from app.routes.task import task_router
from app.routes.org_routes import org_router
from app.routes.mnc_routes import mnc_router
from app.routes.routes import router

# app = FastAPI(__name__)
app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(employee_router)
app.include_router(task_router)
app.include_router(org_router)
app.include_router(mnc_router)
app.include_router(router)


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)

