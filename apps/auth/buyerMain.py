from fastapi import  Depends,HTTPException,status,APIRouter,UploadFile
import random
from models.allModels import Buyers
from schemas.buyers.buyerSchema import BuyerIn, BuyerOut
from utils.users.utills import profile_picture_upload
from config.database import get_db
from sqlalchemy.orm import Session 
from utils.users.utills import hash
from utils.users.email import account_purchased
from typing import List
from .oauth import get_current_user


router= APIRouter(
  tags=["Buyers"]
)


"""
User sign up

"""
def generate_custom_id(prefix: str, n_digits: int) -> str:
    """Generate a custom ID with a given prefix and a certain number of random digits"""
    random_digits = ''.join([str(random.randint(0,9)) for i in range(n_digits)])
    return f"{prefix}{random_digits}"


@router.post('/buyer/signup/', status_code=status.HTTP_201_CREATED)
async def new_buyer ( buyer: BuyerIn= Depends(), file: UploadFile = (None) , db: Session = Depends(get_db)):
  check_email= db.query(Buyers).filter(Buyers.email == buyer.email).first()
  check_username= db.query(Buyers).filter(Buyers.username == buyer.username).first()
  if check_email : 
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email already in use")
  if check_username : 
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Username is taken")
  hashed_password = hash(buyer.password)
  buyer.password = hashed_password
  custom_id = generate_custom_id("BU", 5)
  profile_picture = await profile_picture_upload(file)
  new_account = Buyers(buyer_id=custom_id, profile_picture=profile_picture, **buyer.dict())
  db.add(new_account)
  db.commit()
  db.refresh(new_account)
  await account_purchased("Registration Successful", buyer.email, {
  "title": "Sign up Successful",
  "name": buyer.full_name,
  
})
  return new_account

"""
To fetch all buyers
"""
@router.get('/buyer/',response_model=List[BuyerOut])
async def get_all_buyers( db: Session = Depends(get_db)):
  user_details = db.query(Buyers).all()
  return user_details



"""
To fetch a single buyer
"""
@router.get('/buyer/{id}',response_model=BuyerOut)
async def get_buyer(id: str, db: Session = Depends(get_db), current_user: BuyerOut = Depends(get_current_user)):
  user_details = db.query(Buyers).filter(Buyers.buyer_id == id).first()
  if not user_details:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No buyer with: {id} found")
  return user_details



"""
To delete an buyer
"""

@router.delete("/buyer/{buyer_id}")
async def delete_buyer(buyer_id: str, db: Session = Depends(get_db)):
  # Check if the buyer exists
  buyer = db.query(Buyers).filter(Buyers.buyer_id == buyer_id).first()
  if not buyer:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No buyer with ID: {buyer_id} found")
  
  # Delete the buyer from the database
  db.delete(buyer)
  db.commit()

  return {"message": f"buyer with ID: {buyer_id} deleted successfully"}

# """
# To Update a single buyer
# """

# @router.put('/buyer/{buyer_id}', response_model=BuyerOut)
# async def update_user(
#     buyer_id: str,
#     user_update: UserUpdate,
#     db: Session = Depends(get_db),
#     current_user: BuyerOut = Depends(get_current_user)
# ):
#     existing_user = db.query(Buyers).filter(Buyers.buyer_id == buyer_id).first()

#     if not existing_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {buyer_id} not found")

#     # Update buyer details
#     for field, value in user_update.dict().items():
#         setattr(existing_user, field, value)

#     db.commit()
#     db.refresh(existing_user)

#     return existing_user

