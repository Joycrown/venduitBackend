from fastapi import  Depends,HTTPException,status,APIRouter, UploadFile
import random
from models.allModels import Vendors, UserSignUp, Store
from schemas.vendors.vendorSchema import VendorIn, VendorOut
from config.database import get_db
from sqlalchemy.orm import Session 
from typing import List
from .auth import get_current_user
from utils.users.utills import profile_picture_upload




router= APIRouter(
    tags=["Vendor Auth"]
)


"""
Service Provider sign up

"""
def create_store(name: str, vendor_id: int, db: Session = Depends(get_db)):
  db_vendor = db.query(Vendors).filter(Vendors.vendor_id == vendor_id).first()
  if db_vendor is None:
      raise HTTPException(status_code=404, detail="Vendor not found")
  db_store = Store(store_name=name, vendor_id=vendor_id)
  db.add(db_store)
  db.commit()
  db.refresh(db_store)
  return db_store

@router.patch('/vendor/signup', status_code=status.HTTP_200_OK)
async def update_vendor ( vendor: VendorIn= Depends(), 
  file: UploadFile = (None) , db: Session = Depends(get_db), 
  current_user: Vendors = Depends(get_current_user)):
  try:
    check_user= db.query(Vendors).filter(Vendors.email == current_user.email).first()
    if not check_user : 
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User doesn't exist")
    if current_user.user_type != "vendor":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Operation not allowed for this user as a {current_user.user_type}")

    existing_user = db.query(Vendors).filter(Vendors.vendor_id == current_user.vendor_id).first()
    if not existing_user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.vendor_id} not found")
    
    # Check if the provided username is already taken
    check_username = db.query(Vendors).filter(Vendors.username == vendor.username).first()
    
    if check_username:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username is taken")
    if file:
      profile_picture = await profile_picture_upload(file)
      existing_user.profile_picture = profile_picture

    for field, value in vendor.dict(exclude_unset=True).items():
      setattr(existing_user, field, value)
    db.commit()
    db.refresh(existing_user)


    # Create store for vendor
    store_name = f"{existing_user.username}'s Store"
    create_store(name=store_name, vendor_id=existing_user.vendor_id, db=db)
    existing_user.store_name= store_name
    existing_user.is_verified = True
    
    db.commit()
    db.refresh(existing_user)
    return {"message": f"User {check_user.vendor_id} is updated successfully and store {store_name} is created."}


  except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
  


"""
To fetch all users
"""
@router.get('/vendors',response_model=List[VendorOut])
async def get_all_vendor( db: Session = Depends(get_db)):
  user_details = db.query(Vendors).all()
  return user_details



"""
To fetch a single vendor
"""
@router.get('/vendor/{id}',response_model=VendorOut)
async def get_vendor(id: str, db: Session = Depends(get_db),current_user: VendorOut = Depends(get_current_user)):
  try:
    user_details = db.query(Vendors).filter(Vendors.vendor_id== id).first()
    if not user_details:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No vendor with: {id} found")
    return user_details
  except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))


"""
To delete an vendor
"""

@router.delete("/vendor/{vendor_id}")
async def delete_vendor(vendor_id: str, db: Session = Depends(get_db)):
  try:
    # Check if the vendor exists
    user = db.query(UserSignUp).filter(UserSignUp.user_id == vendor_id).first()
    vendor = db.query(Vendors).filter(Vendors.vendor_id == vendor_id).first()
    if not vendor and not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No vendor with ID: {vendor_id} found")
    
    # Delete the vendor from the database
    if user:
      db.delete(user)
    if vendor:
      db.delete(vendor)
      
    db.commit()

    return {"message": f"vendor with ID: {vendor_id} deleted successfully"}
  except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))


