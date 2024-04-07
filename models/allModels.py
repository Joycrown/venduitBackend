from config.database import Base
from sqlalchemy import Column, Enum, String,Numeric,Float,Boolean,Date,ForeignKey,JSON,LargeBinary
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from enum import Enum 



class UserSignUp(Base):
  __tablename__ = 'users'

  user_id = Column(String, unique=True,primary_key=True, nullable=False)
  email = Column(String, unique=True,primary_key=True, nullable=False)
  full_name = Column(String, nullable=False)
  password = Column(String, nullable=False)
  user_type = Column(String,nullable=False)




class Buyers(Base):
  __tablename__ = 'buyers'

  buyer_id = Column(String, unique=True,primary_key=True, nullable=False)
  full_name = Column(String, nullable=False)
  username = Column(String,nullable=False, unique=True, server_default="N/A")
  date_of_birth = Column(String,nullable=False, server_default="N/A")
  email = Column(String,nullable=False, unique=True)
  city = Column(String,nullable=False, server_default="N/A")
  gender = Column(String,nullable=False, server_default="N/A")
  country = Column(String,nullable=False, server_default="N/A")
  password = Column(String,nullable=False)
  phone_no = Column(String,nullable=False, server_default="N/A")
  bought_fake= Column(String,nullable=False, server_default="N/A")
  social_media_platform = Column(JSON,default={"default_key": "N/A"})
  is_scammed = Column (String, nullable=False, server_default="N/A")
  use_venduit = Column (String, nullable=False, server_default="N/A")
  is_verified = Column (Boolean,nullable=False, default=False)
  shopping = Column(String,nullable=False, server_default="N/A")
  profile_picture = Column(String, nullable=False, server_default="N/A")
  user_type = Column(String,nullable=False, server_default="buyer")
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))





class Vendors(Base):
  __tablename__ = 'vendors'

  vendor_id = Column(String, unique=True,primary_key=True, nullable=False)
  full_name = Column(String, nullable=False)
  username = Column(String,nullable=False,unique=True, server_default="N/A")
  date_of_birth = Column(String,nullable=False, server_default="N/A")
  email = Column(String,nullable=False, unique=True)
  gender = Column(String,nullable=False, server_default="N/A")
  city = Column(String,nullable=False, server_default="N/A")
  password = Column(String,nullable=False)
  phone_no = Column(String,nullable=False, server_default="N/A")
  business_name = Column(String,nullable=False,unique=True, server_default="N/A")
  business_bio = Column(String,nullable=False, server_default="N/A")
  business_category = Column(String,nullable=False, server_default="N/A")
  business_reach = Column(String,nullable=False, server_default="N/A")
  business_social_links = Column(JSON, default={"default_key": "N/A"})
  business_startDate = Column(String,nullable=False, server_default="N/A")
  business_logo = Column(String,nullable=False,server_default="N/A")
  is_scammed = Column (String, nullable=False, server_default="N/A")
  use_venduit = Column (String, nullable=False, server_default="N/A")
  is_verified = Column (Boolean,nullable=False, default=False)
  country = Column(String,nullable=False, server_default="N/A")
  profile_picture = Column(String, nullable=False, server_default="N/A")
  user_type = Column(String,nullable=False, server_default="vendor")
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
