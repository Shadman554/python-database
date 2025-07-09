from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: str
    is_active: bool
    is_admin: bool
    total_points: int
    today_points: int
    created_at: datetime
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Book schemas
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    cover_url: Optional[str] = None
    download_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str
    added_at: datetime
    
    class Config:
        from_attributes = True

# Disease schemas
class DiseaseBase(BaseModel):
    name: str
    kurdish: Optional[str] = None
    symptoms: Optional[str] = None
    cause: Optional[str] = None
    control: Optional[str] = None

class DiseaseCreate(DiseaseBase):
    pass

class Disease(DiseaseBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Drug schemas
class DrugBase(BaseModel):
    name: str
    usage: Optional[str] = None
    side_effect: Optional[str] = None
    other_info: Optional[str] = None
    drug_class: Optional[str] = None

class DrugCreate(DrugBase):
    pass

class Drug(DrugBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dictionary schemas
class DictionaryWordBase(BaseModel):
    name: str
    kurdish: Optional[str] = None
    arabic: Optional[str] = None
    description: Optional[str] = None
    barcode: Optional[str] = None
    is_saved: bool = False
    is_favorite: bool = False

class DictionaryWordCreate(DictionaryWordBase):
    pass

class DictionaryWord(DictionaryWordBase):
    id: str
    
    class Config:
        from_attributes = True

# Question schemas
class QuestionBase(BaseModel):
    text: str
    user_name: str
    user_email: str
    user_photo: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: str
    user_id: str
    likes: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Notification schemas
class NotificationBase(BaseModel):
    title: str
    body: str
    image_url: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Staff schemas
class StaffBase(BaseModel):
    name: str
    job: str
    description: Optional[str] = None
    photo: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    snapchat: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: str
    
    class Config:
        from_attributes = True

# Tutorial Video schemas
class TutorialVideoBase(BaseModel):
    title: str
    video_id: str

class TutorialVideoCreate(TutorialVideoBase):
    pass

class TutorialVideo(TutorialVideoBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Normal Range schemas
class NormalRangeBase(BaseModel):
    name: str
    species: str
    category: str
    unit: str
    min_value: str
    max_value: str

class NormalRangeCreate(NormalRangeBase):
    pass

class NormalRange(NormalRangeBase):
    id: str
    
    class Config:
        from_attributes = True

# App Link schemas
class AppLinkBase(BaseModel):
    url: str

class AppLinkCreate(AppLinkBase):
    pass

class AppLink(AppLinkBase):
    id: str
    
    class Config:
        from_attributes = True

# About schemas
class AboutBase(BaseModel):
    text: str

class AboutCreate(AboutBase):
    pass

class About(AboutBase):
    id: str
    exported_at: datetime
    
    class Config:
        from_attributes = True

# Common response schemas
class PaginatedResponse(BaseModel):
    items: List[BaseModel]
    total: int
    page: int
    size: int
    pages: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
