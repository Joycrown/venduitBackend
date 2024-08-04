from datetime import datetime
from typing import Optional,List,Union
from pydantic import BaseModel, EmailStr

class ProductIn(BaseModel):
  product_name:str
  product_description:str
  product_price: int



class ProductOut(BaseModel):
  id: int
  product_name: str
  product_description: str
  product_price: int
  store_name: str

  class Config:
    from_attributes = True




class StoreOut(BaseModel):
  id: int
  vendor_id:str
  store_name :str
  store_product: Union[ProductOut, List[ProductOut]]

  class Config:
    from_attributes = True
  




