from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class SignUpSchema(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: EmailStr
    phone_number: str
    password: str
    conf_password: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "first_name": "Jasmin",
                "last_name": "Nimadir",
                "username": "axorip",
                "email": "Jasminanematullayeva1210005@gmail.com",
                "phone_number": "+998901234567",
                "password": "1210!",
                "conf_password": "1210!"
            }
        }
    }


class LoginSchema(BaseModel):
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }

class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = Field(default=None)
    phone_number: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str
    conf_password: str

    model_config = {
        "from_attributes": True
    }

class Settings(BaseModel):
    authjwt_secret_key: str = '07cb894119b107b905293969cb32ed1ba06c5da89576452badf61fda301a9241'   
    authjwt_access_token_expires : timedelta = timedelta(minutes=40)
    authjwt_refresh_token_expires : timedelta = timedelta(days=1)