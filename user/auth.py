import re
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth2 import AuthJWT
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from .models import User
from .schema import SignUpSchema, LoginSchema
from fastapi_jwt_auth2.exceptions import AuthJWTException

def check_user(db: Session, column, value):
    user = db.query(User).filter(column == value).first()
    if user:
        raise HTTPException(status_code=400, detail=f'Bu {value} allaqachon mavjud')

def check_pass(password, conf_password=None):

    if not password or not conf_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg': "Parol va tasdiqlash maydoni toldirilishi shart"}
        )
    
    regex = re.fullmatch(
        re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"), 
        password
    )
    
    if not regex:
        raise HTTPException(status_code=400, detail='Parol yaroqsiz')
    
    if password and conf_password and password != conf_password:
        raise HTTPException(status_code=400, detail='Parollar mos kelmadi')

    
        
    return True


def register(new_user: SignUpSchema, db: Session):
    check_user(db, User.username, new_user.username)
    check_user(db, User.email, new_user.email)
    check_user(db, User.phone_number, new_user.phone_number)
    check_pass(new_user.password, new_user.conf_password)

    user = User(
        first_name = new_user.first_name,
        last_name = new_user.last_name,
        username = new_user.username,
        email = new_user.email,
        phone_number = new_user.phone_number,
        password = generate_password_hash(new_user.password)  
    )
    

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "msg": 'Register',
        'status': status.HTTP_201_CREATED
    }


def login(data: LoginSchema, db: Session, Authorize: AuthJWT):
    db_user = db.query(User).filter(User.username == data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Bu username majud emas')

    if not check_password_hash(db_user.password, data.password):
        raise HTTPException(status_code=400, detail='Parol xato')

    refresh_token = Authorize.create_refresh_token(subject=str(db_user.id))
    access_token = Authorize.create_access_token(subject=str(db_user.id))

    print("ACCESS TOKEN TYPE:", type(access_token))
    print("ACCESS TOKEN VALUE:", access_token)

    return {
        "msg": 'login',
        'access': access_token.decode() if isinstance(access_token, bytes) else access_token,
        'refresh': refresh_token.decode() if isinstance(refresh_token, bytes) else refresh_token,
    }


def get_profile(Authorize: AuthJWT, db: Session):
    try:
        Authorize.jwt_required()  
    except AuthJWTException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": e.message}
        ) 
    current_user_id = Authorize.get_jwt_subject()
    
    user = db.query(User).filter(User.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Foydalanuvchi topilmadi"}
        )
    return user