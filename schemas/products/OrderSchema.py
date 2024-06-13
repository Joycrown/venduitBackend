from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr,Field
from schemas.vendors.vendorSchema import VendorOut
from fastapi import UploadFile



class ProductSchema(BaseModel):
  product_name: str
  product_desc: str
  amount: int
  product_image: Optional[UploadFile] = Field(default=None, description="Product image file")


class OrderRequest(BaseModel):
  vendor_id : str
  products: List[ProductSchema]
    

class CreateOrderNonVenduit(BaseModel):

  product_name: str
  quantity : int
  price : str

class OrderSummaryOut(BaseModel):
    vendor_name: str
    status: str
    price: float
    order_id: str

class OrderItemOut(BaseModel):
  order_id : str
  product_name : str
  product_desc :str
  price : int
  product_image :str




class OrderOut(BaseModel):
  order_id : str
  status: str
  is_dispute: bool
  buyer_id : str
  vendor_id: str
  ordered: List[OrderItemOut]
  vendor: VendorOut
  created_at: datetime
  

class OrderItemOut(BaseModel):
  order_id: str
  product_name: str
  product_desc: str
  price: str
  product_image: str
