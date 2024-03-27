from datetime import datetime
import email
from typing import Optional,List
from pydantic import BaseModel, EmailStr




class VendorIn(BaseModel):

  full_name: str
  username: str
  email: EmailStr
  password:str
  city : str
  country: str
  gender: str
  date_of_birth: str
  is_scammed: str
  use_venduit: str
  phone_no: str
  business_name: str
  business_bio: str
  business_category: str
  business_reach: str
  business_social_links: List[str]
  business_startDate: str
 
  
  

class VendorOut(BaseModel):

  vendor_id: str
  full_name: str
  username: str
  email: EmailStr
  city : str
  country: str
  gender: str
  date_of_birth: str
  is_scammed: str
  use_venduit: str
  phone_no: str
  user_type: str
  is_verified: bool
  business_name: str
  business_category: str
  business_reach: str
  business_social_links: List[str]
  business_startDate: str
  created_at : datetime


  class Config:
    from_attributes = True




# class UserUpdate(BaseModel):

#   full_name: Optional[str]
#   type: Optional[str]
#   phone_no: Optional [str]
#   company_name: Optional[str]
#   company_url: Optional[str]





