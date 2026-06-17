from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth2 import AuthJWT
from sqlalchemy.orm import Session
from db import get_db
from users.schema import SignUpSchema, LoginSchema, UserResponseSchema
from users import auth

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def auth_register(new_user: SignUpSchema, db: Session = Depends(get_db)):
    return auth.register(new_user, db)


@router.post("/login")
def auth_login(data: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.login(data, db, Authorize)


@router.get("/profile", response_model=UserResponseSchema)
def auth_profile(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return auth.get_profile(Authorize, db)

