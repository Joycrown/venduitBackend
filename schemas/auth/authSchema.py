
from pydantic import BaseModel, EmailStr

from config.database import Base




class UserLogin(BaseModel):
  email: str
  password: str



class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  id: str
  email: EmailStr



class PasswordResetTokenData(BaseModel):
  email: EmailStr



class CurrentUser(BaseModel):
  user_id: str
  full_name: str
  username: str
  email: str
  phone_no: int
  user_type: str
 



class EmailReset(BaseModel):
  email: EmailStr



class  ResetPassword(BaseModel):
  new_password:str
  token : str



class UpdatePassword(BaseModel):
  current_password: str
  new_password: str

   