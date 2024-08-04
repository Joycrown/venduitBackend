from fastapi import  Depends,HTTPException,status,APIRouter,Query
import random
from models.allModels import Orders,Vendors,OrderItem
from schemas.buyers.buyerSchema import BuyerIn, BuyerOut, UserSignUpIn
from schemas.vendors.vendorSchema import  VendorOut
from utils.users.utills import product_image_upload
from config.database import get_db
from sqlalchemy.orm import Session
from apps.auth.oauth import create_token_signup_vendor
from utils.users.email import order_created_buyer,order_created_vendor_nonVenduit,order_created_vendor_venduit
from typing import List, Optional,Annotated
from pydantic import EmailStr
from apps.auth.oauth import get_current_user


router= APIRouter(
  tags=["Buyer Operations"]
)

@router.get('/search_vendor', response_model=List[VendorOut])
def search_vendor_by_name_or_username(search: Optional[str] = Query(None, title="Search vendor by full name or username"), 
                                      db: Session = Depends(get_db), 
                                      current_user: BuyerOut = Depends(get_current_user)):
    try:
      if current_user.user_type != "buyer":
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Operation not allowed for this user as a {current_user.user_type}")

      if search:
          vendors = db.query(Vendors).filter(
              Vendors.full_name.ilike(f"%{search}%") |
              Vendors.username.ilike(f"%{search}%")
          ).all()
      else:
          vendors = db.query(Vendors).all()
          random.shuffle(vendors)
          vendors = vendors[:10]  # Return a limited number of random vendors, e.g., 10

      return vendors
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))



