from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_models import UserModel
from app.schemas.user_schema import UserSignupSchema, UserLoginSchema, UserResponseSchema
from app.utils.user_utils import UserUtils

user_utils = UserUtils()


class UserServiceClass:

    @staticmethod
    def user_signup_service(db: Session, user_data: UserSignupSchema):
        existing_user = db.query(UserModel).filter(
            (UserModel.username == user_data.username) | (UserModel.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already registered")
        hashed_password = user_utils.get_password_hash(user_data.password)
        db_user = UserModel(
            username=user_data.username,
            email=str(user_data.email),
            full_name=user_data.full_name,
            gender=user_data.gender,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def user_login_service(db: Session, user_data: UserLoginSchema):
        db_user = db.query(UserModel).filter(
            (UserModel.username == user_data.username) | (UserModel.email == user_data.username)).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user_utils.verify_password(user_data.password, str(db_user.hashed_password)):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = UserUtils.create_access_token({"sub": str(db_user.id), "role": db_user.role.value,"username":db_user.username})
        user_response_data = UserResponseSchema.from_orm(db_user)
        return {"token": access_token, "user": user_response_data}
