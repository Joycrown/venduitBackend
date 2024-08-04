from fastapi import  Depends,HTTPException,status,APIRouter,UploadFile,File, Form
import random
from models.allModels import Orders,Vendors,OrderItem
from schemas.buyers.buyerSchema import BuyerOut
from schemas.products.OrderSchema import  CreateOrderNonVenduit,OrderOut, OrderSummaryOut
from utils.users.utills import product_image_upload
from config.database import get_db
from sqlalchemy.orm import Session
from apps.auth.oauth import create_token_signup_vendor
from utils.users.email import order_created_buyer,order_created_vendor_nonVenduit,order_created_vendor_venduit
from typing import List
from pydantic import EmailStr
from apps.auth.oauth import get_current_user


router= APIRouter(
  tags=["Orders"]
)


def generate_custom_id(prefix: str, n_digits: int) -> str:
    """Generate a custom ID with a given prefix and a certain number of random digits"""
    random_digits = ''.join([str(random.randint(0,9)) for _ in range(n_digits)])
    return f"{prefix}{random_digits}"

"""
Creating an order or payment request by the buyer to a vendor on venduit
"""
# Helper functions
def get_vendor_by_id(db: Session, vendor_id: str):
    return db.query(Vendors).filter(Vendors.vendor_id == vendor_id).first()

def generate_order_id(prefix: str, length: int):
    # Assuming this function generates a custom ID
    return generate_custom_id(prefix, length)

async def upload_product_image(image: UploadFile):
    # Assuming this function uploads the product image and returns the file path
    return await product_image_upload(image)

def create_order_in_db(db: Session, buyer_id: str, vendor_id: str):
    order_id = generate_order_id("TR", 7)
    order = Orders(order_id=order_id, buyer_id=buyer_id, vendor_id=vendor_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def create_order_items(db: Session, order_id: str, product_data: List[dict]):
    order_items = []
    for item_data in product_data:
        order_item = OrderItem(order_id=order_id, **item_data)
        db.add(order_item)
        order_items.append(order_item)
    db.commit()
    return order_items

async def notify_users(order_id: str, buyer_email: str, buyer_name: str, vendor_email: str, vendor_name: str):
    await order_created_buyer("Order and Payment created Successfully", buyer_email, {
        "title": "Payment Successfully made",
        "name": buyer_name,
    })
    await order_created_vendor_venduit("You have a new payment/order from Venduit", vendor_email, {
        "title": "New Payment",
        "name": vendor_name,
    })

# Endpoint
@router.post('/create_order', status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order_vendor(
    vendor_id: str = Form(...), 
    product_name: List[str] = Form(...), 
    product_desc: List[str] = Form(...), 
    amount: List[str] = Form(...), 
    product_images: List[UploadFile] = File(...), 
    db: Session = Depends(get_db), 
    current_user: BuyerOut = Depends(get_current_user)
):
    try:
        if current_user.user_type != 'buyer':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only a buyer can create an order")

        vendor = get_vendor_by_id(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Vendor with ID {vendor_id} found")

        order = create_order_in_db(db, current_user.buyer_id, vendor_id)

        order_items_data = []
        for name, desc, amt, image in zip(product_name, product_desc, amount, product_images):
            names = name.split(',')
            descs = desc.split(',')
            amts = amt.split(',')
            for n, d, a in zip(names, descs, amts):
                product_image_path = await upload_product_image(image)
                order_item_data = {
                    "product_name": n.strip(),
                    "product_desc": d.strip(),
                    "price": a.strip(),
                    "product_image": product_image_path
                }
                order_items_data.append(order_item_data)

        full_order = create_order_items(db, order.order_id, order_items_data)

        await notify_users(order.order_id, current_user.email, current_user.full_name, vendor.email, vendor.full_name)

        return {
            "message": "Order Created",
            "order_id": order.order_id,
            "status": order.status,
            "is_dispute": order.is_dispute,
            "buyer_id": order.buyer_id,
            "vendor_id": order.vendor_id,
            "ordered": full_order,
            "vendor": vendor,
            "created_at": order.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



"""
Creating an order or payment request by the buyer to a vendor not venduit
"""
@router.post('/create_order_non_venduit', status_code=status.HTTP_201_CREATED)
async def create_order_non_vendor (vendor_full_name : str, order: CreateOrderNonVenduit= Depends(), 
  vendor_email: EmailStr =(None), vendor_phone_no: str=(None), product_desc: str=(None),
  file: UploadFile = (None), db:Session=Depends(get_db),
  current_user: BuyerOut = Depends(get_current_user)):
  if current_user.user_type != 'buyer':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="only a buyer a can create an order")
  if vendor_email:
    find_vendor = db.query(Vendors).filter(Vendors.email==vendor_email).first()
    if find_vendor:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="The vendor with the mail exist already.")
  custom_id = generate_custom_id("TR",7)
  #check if either email or phone is present  else set it as none
  if not (vendor_email or vendor_phone_no):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Vendor contact included")
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



"""
Getting the vendor name and the price of an order to render as a transaction in the frontend
"""
@router.get('/get_orders', response_model=List[OrderSummaryOut], status_code=status.HTTP_200_OK)
async def get_orders(db: Session = Depends(get_db), current_user: BuyerOut = Depends(get_current_user)):
    try:
      if current_user.user_type != 'buyer':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only buyers can get the list of transactions")

      # Joining Orders with Vendors and OrderItems and filtering by buyer_id
      orders = db.query(Orders.order_id, Orders.status, Vendors.full_name, OrderItem.price).\
                  join(Vendors, Vendors.vendor_id == Orders.vendor_id).\
                  join(OrderItem, OrderItem.order_id == Orders.order_id).\
                  filter(Orders.buyer_id == current_user.buyer_id).\
                  all()

      # Transforming data into the desired output format
      results = [{"vendor_name": vendor_name, "status": status, "price": price, "order_id": order_id} for order_id, status, vendor_name, price in orders]
      
      # Return the results directly, an empty list will be returned if no orders are found
      return results
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))