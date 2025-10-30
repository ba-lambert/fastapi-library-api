from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_app_db
from app.enums.role_enum import RoleEnum
from app.schemas.user_schema import UserSignupSchema, UserLoginSchema
from app.services.user_service import UserServiceClass

user_router = APIRouter(tags=['user'])

user_service = UserServiceClass()


@user_router.post('/signup')
def user_signup(user_data: UserSignupSchema, db: Session = Depends(get_app_db)):
    return user_service.user_signup_service(db, user_data)

@user_router.post('/login')
def user_login(user_data: UserLoginSchema, db: Session = Depends(get_app_db)):
    return user_service.user_login_service(db,user_data)

@user_router.put('/assign-role/{id}')
def user_assign_role(id:UUID,role:RoleEnum,db:Session=Depends(get_app_db)):
    return user_service.user_assign_role_service(db,id,role)