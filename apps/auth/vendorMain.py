from fastapi import  Depends,HTTPException,status,APIRouter, UploadFile
import random
from models.allModels import Vendors
from schemas.vendors.vendorSchema import VendorIn, VendorOut
from config.database import get_db
from sqlalchemy.orm import Session 
from utils.users.utills import hash
from typing import List
from utils.users.email import account_purchased
from .auth import get_current_user
from utils.users.utills import profile_picture_upload, business_logo_upload




router= APIRouter(
    tags=["Vendor"]
)


"""
Service Provider sign up

"""
def generate_custom_id(prefix: str, n_digits: int) -> str:
    """Generate a custom ID with a given prefix and a certain number of random digits"""
    random_digits = ''.join([str(random.randint(0,9)) for i in range(n_digits)])
    return f"{prefix}{random_digits}"


@router.post('/vendor/signup/', status_code=status.HTTP_201_CREATED, response_model=VendorOut)
async def new_vendor (vendor:VendorIn = Depends(), profilePicture: UploadFile = (None), logo: UploadFile = (None), db: Session = Depends(get_db)):
    check_email= db.query(Vendors).filter(Vendors.email == vendor.email).first()
    check_username= db.query(Vendors).filter(Vendors.username == vendor.username).first()
    check_business_name= db.query(Vendors).filter(Vendors.business_name == vendor.business_name).first()
    if check_email: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
    if check_username: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"username is taken")
    if check_business_name: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"business name is taken")
    hashed_password = hash(vendor.password)
    vendor.password = hashed_password
    custom_id = generate_custom_id("SL", 5)
    profile_picture = await profile_picture_upload(profilePicture)
    business_logo = await business_logo_upload(logo)
    new_account = Vendors(vendor_id=custom_id, business_logo=business_logo, profile_picture=profile_picture, **vendor.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    await account_purchased("Registration Successful", vendor.email, {
    "title": "Account Purchase Successful",
    "name": vendor.full_name,
    
  })
    return  new_account

"""
To fetch all users
"""
@router.get('/vendor/',response_model=List[VendorOut])
async def get_all_vendor( db: Session = Depends(get_db)):
  user_details = db.query(Vendors).all()
  return user_details



"""
To fetch a single vendor
"""
@router.get('/vendor/{id}',response_model=VendorOut)
async def get_vendor(id: str, db: Session = Depends(get_db),current_user: VendorOut = Depends(get_current_user)):
  user_details = db.query(Vendors).filter(Vendors.vendor_id== id).first()
  if not user_details:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No vendor with: {id} found")
  return user_details



"""
To delete an vendor
"""

@router.delete("/vendor/{vendor_id}")
async def delete_vendor(vendor_id: str, db: Session = Depends(get_db)):
  # Check if the vendor exists
  vendor = db.query(Vendors).filter(Vendors.vendor_id == vendor_id).first()
  if not vendor:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No vendor with ID: {vendor_id} found")
  
  # Delete the vendor from the database
  db.delete(vendor)
  db.commit()

  return {"message": f"vendor with ID: {vendor_id} deleted successfully"}

# """
# To Update a vendor
# """

# @router.put('/vendor/{vendor_id}', response_model=VendorOut)
# async def update_user(
#     vendor_id: str,
#     user_update: VendorUpdate,
#     db: Session = Depends(get_db),
#     current_user: VendorOut = Depends(get_current_user)
# ):
#     existing_user = db.query(vendor).filter(vendor.vendor_id == vendor_id).first()

#     if not existing_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {vendor_id} not found")

#     # Check if the new phone number is already in use
#     if user_update.phone_no and user_update.phone_no != existing_user.phone_no:
#         existing_phone = db.query(vendor).filter(vendor.phone_no == user_update.phone_no).first()
#         if existing_phone:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Phone number {user_update.phone_no} is already in use")

#     # Update vendor details
#     for field, value in user_update.dict().items():
#         setattr(existing_user, field, value)

#     db.commit()
#     db.refresh(existing_user)

#     return existing_user

