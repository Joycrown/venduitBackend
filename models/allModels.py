from config.database import Base
from sqlalchemy import Column,String,Boolean,JSON,Integer, ForeignKey, Float
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
  username = Column(String,nullable=False, server_default="N/A")
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
  username = Column(String,nullable=False, server_default="N/A")
  date_of_birth = Column(String,nullable=False, server_default="N/A")
  email = Column(String,nullable=False, unique=True)
  gender = Column(String,nullable=False, server_default="N/A")
  city = Column(String,nullable=False, server_default="N/A")
  password = Column(String,nullable=False)
  phone_no = Column(String,nullable=False, server_default="N/A")
  business_name = Column(String,nullable=False, server_default="N/A")
  business_bio = Column(String,nullable=False, server_default="N/A")
  business_category = Column(String,nullable=False, server_default="N/A")
  business_reach = Column(String,nullable=False, server_default="N/A")
  business_social_links = Column(JSON, default={"default_key": "N/A"})
  business_startDate = Column(String,nullable=False, server_default="N/A")
  business_logo = Column(String,nullable=False,server_default="N/A")
  is_scammed = Column (String, nullable=False, server_default="N/A")
  use_venduit = Column (String, nullable=False, server_default="N/A")
  store_name = Column (String, ForeignKey("stores.store_name", ondelete="CASCADE"), nullable=True)
  is_verified = Column (Boolean, nullable=False, default=False)
  country = Column(String,nullable=False, server_default="N/A")
  profile_picture = Column(String, nullable=False, server_default="N/A")
  user_type = Column(String,nullable=False, server_default="vendor")
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
  store = relationship("Store", foreign_keys=[store_name])


class Orders(Base):
  __tablename__ = 'orders'

  order_id = Column(String, primary_key=True, unique=True, index=True)
  status = Column(String, nullable=False, default="Ordered")
  is_dispute = Column(Boolean, nullable=False, default=False)
  buyer_id = Column(String, ForeignKey("buyers.buyer_id", ondelete="CASCADE"), nullable=False)
  buyer = relationship('Buyers')
  vendor_id = Column(String, ForeignKey("vendors.vendor_id", ondelete="CASCADE"), nullable=True)
  vendor = relationship('Vendors')
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")

  items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
  __tablename__ = 'order_items'

  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(String, ForeignKey('orders.order_id'))
  product_name = Column(String, nullable=False)
  product_desc = Column(String, nullable=True, default="N/A")
  price = Column(String, nullable=False)
  product_image = Column(String, nullable=False, default="N/A")

  order = relationship("Orders", back_populates="items")



class Disputes(Base):
  __tablename__ = 'disputes'

  dispute_id = Column(String, unique=True,primary_key=True, nullable=False)
  dispute_category = Column(String, nullable=False)
  dispute_desc = Column(String, nullable=True, server_default="N/A")
  status = Column(String, nullable=False, server_default="N/A")
  dispute_image = Column(String, nullable=False, server_default="N/A")
  order_id  = Column(String,ForeignKey("orders.order_id",ondelete="CASCADE"), nullable=False)
  order= relationship('Orders',foreign_keys=[order_id])
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))



class Store(Base):
  __tablename__ = 'stores'

  id = Column(Integer, primary_key=True, unique=True, index=True)
  store_name = Column(String, unique=True, nullable=False)
  vendor_id = Column(String, ForeignKey('vendors.vendor_id'))
  vendor = relationship("Vendors", foreign_keys=[vendor_id])
  product_id = Column(Integer, ForeignKey('products.id'))
  store_product = relationship("Product",foreign_keys=[product_id])




class Product(Base):
  __tablename__ = 'products'

  id = Column(Integer, primary_key=True,unique=True, index=True)
  product_name = Column(String, unique=True, nullable=False)
  product_description = Column(String, nullable=False)
  product_price = Column(Integer, nullable=False)
  store_name = Column(String, ForeignKey('stores.store_name'))
 



class Rating(Base):
  __tablename__ = 'ratings'

  id = Column(Integer, primary_key=True,unique=True, index=True)
  value = Column(Float, nullable=False, default=0.0)
  vendor_id = Column(String, ForeignKey('vendors.vendor_id'))
  vendor = relationship("Vendors", foreign_keys=[vendor_id])