from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CreateAuthorSchema(BaseModel):
    name : Optional[str] = None
    year: int
    
    class Config:
        from_attribute=True
        extra_kwargs = {
            'name': 'Nimadir',
            'year': 2005
        }
        
class AuthorAut(CreateAuthorSchema):
    pass
    
    
class UpdateAuthorSchema(CreateAuthorSchema):
    year: Optional[int] = None
    
    class Config:
        from_attribute=True

    
class CreateCategorySchema(BaseModel):
    title : str = Field(max_length=100)
    class Config:
        from_attribute=True
    
class UpdateCategorySchema(BaseModel):
    title: Optional[str] = None
    
    class Config:
        from_attribute=True
    

class CreateBookSchema(BaseModel):
    title : str = Field(max_length=200)
    year : Optional[int] = None
    desc : Optional[str] = None
    price : Decimal = Field(max_digits=15, decimal_places=2)
    author_id : int
    category_id : int
    is_published : Optional[bool] = None
    
    class Config:
        from_attribute=True
    
    
class UpdateBookSchema(CreateBookSchema):
    title : Optional[str] = None
    price : Optional[float] = Field(default=None, max_digits=12, decimal_places=2, ge=0)
    author_id : Optional[int] = None
    category_id : Optional[int] = None
    
    class Config:
        from_attribute=True
    

class CreateCommentSchema(BaseModel):
    summary : str = Field(max_length=200)
    user : str
    book_id : int
    
    class Config:
        from_attribute=True
    
    
class UpdateCommentSchema(BaseModel):
    summary : Optional[str]  = Field(default=None, max_length=200)

    class Config:
        from_attribute=True

class CreateSavedSchema(BaseModel):
    user_id : int
    book_id : int
    
    class Config:
        from_attribute=True
        
    
    
    
    
    
    
