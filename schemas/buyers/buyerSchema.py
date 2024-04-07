from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr




class  UserSignUpIn(BaseModel):
  email:EmailStr
  password: str
  full_name: str
  user_type:str

  

# class UserSIgnUpOut(BaseModel):
#   email: EmailStr
  
class BuyerIn(BaseModel):

  username: str
  city : str
  country: str
  gender: str
  date_of_birth: str
  bought_fake : str
  social_media_platform: List[str]
  is_scammed: str
  use_venduit: str
  phone_no: str
  shopping: str
  
  

class BuyerOut(BaseModel):

  buyer_id: str
  full_name: str
  username: str
  email: EmailStr
  city : str
  country: str
  gender: str
  date_of_birth: str
  bought_fake : str
  social_media_platform: List[str]
  is_scammed: str
  use_venduit: str
  phone_no: str
  shopping: str
  profile_picture: str
  user_type: str
  is_verified: bool
  created_at : datetime


  class Config:
    from_attributes = True








