from fastapi import  Depends,HTTPException,status,APIRouter,UploadFile,File, Form
import random
from models.allModels import Orders,Vendors,OrderItem
from schemas.buyers.buyerSchema import BuyerIn, BuyerOut, UserSignUpIn
from schemas.products.OrderSchema import  CreateOrderNonVenduit,ProductSchema, OrderRequest,OrderOut,OrderItemOut
from utils.users.utills import product_image_upload
from config.database import get_db
from sqlalchemy.orm import Session 
from apps.auth.oauth import create_token_signup_vendor
from utils.users.email import order_created_buyer,order_created_vendor_nonVenduit,order_created_vendor_venduit
from typing import List, Optional,Annotated
from pydantic import EmailStr
from apps.auth.oauth import get_current_user


router= APIRouter(
  tags=["Orders"]
)


def generate_custom_id(prefix: str, n_digits: int) -> str:
    """Generate a custom ID with a given prefix and a certain number of random digits"""
    random_digits = ''.join([str(random.randint(0,9)) for i in range(n_digits)])
    return f"{prefix}{random_digits}"

"""
Creating an order or payment request by the buyer to a vendor on venduit
"""
@router.post('/create_order', status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order_vendor(vendor_id: str = Form(...), 
    product_name: List[str] = Form(...), 
    product_desc: List[str] = Form(...), 
    amount: List[str] = Form(...), 
    product_images: List[UploadFile] = File(...), 
    db: Session = Depends(get_db), 
    current_user: BuyerOut = Depends(get_current_user)):
    if current_user.user_type != 'buyer':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only a buyer can create an order")

    find_vendor = db.query(Vendors).filter(Vendors.vendor_id == vendor_id).first()
    if not find_vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Vendor with ID {vendor_id} found")

    custom_id = generate_custom_id("TR", 7)
    order = Orders(order_id=custom_id, buyer_id=current_user.buyer_id, vendor_id=vendor_id)

    db.add(order)
    db.commit()
    db.refresh(order)

   
    order_items = []  # Initialize an empty list to store order items
    full_order = []  # Initialize an empty list to store order items
    # print(product_images)
    for name, desc, amt in zip(product_name, product_desc, amount):
        names = name.split(',')  # Split product_name at the comma
        descs = desc.split(',')  # Split product_desc at the comma
        amts = amt.split(',')    # Split amount at the comma

        for n, d, a,image in zip(names, descs, amts, product_images):
            product_picture = await product_image_upload(image)  # Save the product image and get the file path
            order_item_data = {
                "product_name": n.strip(),   # Strip leading/trailing whitespace from product_name
                "product_desc": d.strip(),   # Strip leading/trailing whitespace from product_desc
                "price": a.strip(),         # Strip leading/trailing whitespace from amount
                "product_image": product_picture  # Assuming product_picture is the image file path
            }
            order_items.append(order_item_data)  # Add the order item data dictionary to the list
    for order_item_data in order_items:
      order_item = OrderItem(order_id= order.order_id, **order_item_data)  # Assuming OrderItem is your SQLAlchemy model for order items
      db.add(order_item) 
      full_order.append(order_item) 
    db.commit()  # Commit the changes to the database
    # db.commit()
    db.refresh(order)
    await order_created_buyer("Order and Payment created Successfully", current_user.email, {
        "title": "Payment Successfully made",
        "name": current_user.full_name,
    })
    await order_created_vendor_venduit("You have a new payment/order from Venduit", find_vendor.email, {
        "title": "New Payment",
        "name": find_vendor.full_name,
    })
    return {"message": "Order Created", "order_id": order.order_id, "status": order.status, "is_dispute": order.is_dispute, "buyer_id": order.buyer_id, "vendor_id": order.vendor_id, "ordered": full_order, "vendor": find_vendor, "created_at": order.created_at}





"""
Creating an order or payment request by the buyer to a vendor not venduit
"""
@router.post('/create_order_non_venduit', status_code=status.HTTP_201_CREATED)
async def create_order_non_vendor (vendor_full_name : str, order: CreateOrderNonVenduit= Depends(), 
  vendor_email: EmailStr =(None), vendor_phone_no: str=(None), product_desc: str=(None),
  file: UploadFile = (None), db:Session=Depends(get_db),
  current_user: BuyerOut = Depends(get_current_user)):
  if current_user.user_type != 'buyer':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"only a buyer a can create an order")
  if vendor_email:
    find_vendor = db.query(Vendors).filter(Vendors.email==vendor_email).first()
    if find_vendor:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="The vendor with the mail exist already.")
  custom_id = generate_custom_id("TR",7)
  #check if either email or phone is present  else set it as none
  if not (vendor_email or vendor_phone_no):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No Vendor contact included")
  if file:
    product_picture = await product_image_upload(file)
  product_picture ="none"

  if vendor_email:
    vendor_email = vendor_email
  if vendor_full_name:
    vendor_name = vendor_full_name
  if vendor_phone_no:
    vendor_phone_no = vendor_phone_no
  if not product_desc:
    product_desc = order.product_name

  token = create_token_signup_vendor(data={"email": vendor_email, "full_name":vendor_full_name ,"user_type": "vendor"})
  link = f'http://localhost:5173/create_vendors/{token}'
  order = Orders(order_id=custom_id, buyer_id=current_user.buyer_id,
  product_image=product_picture, product_desc=product_desc, **order.dict())
  db.add(order)
  db.commit()
  db.refresh(order)
  await order_created_buyer("Order and Payment created Successful", current_user.email, {
  "title": "Payment Successfully made",
  "name": current_user.full_name,
})
  await order_created_vendor_nonVenduit("You have a new payment/order from Venduit", vendor_email, {
  "title": "New Payment",
  "name": vendor_name,
  "product_name": order.product_name,
  "product_desc": order.product_desc,
  "price": order.price,
  "link": link
})
  return {"message":"Order Created", "order":order, "link": link}