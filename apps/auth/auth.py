from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from config.database import get_db
from models.allModels import Buyers, Vendors, UserSignUp
from utils.users.utills import verify, hash
from apps.auth.oauth import get_current_user, create_password_reset_token, create_tokens, verify_refresh_token,verify_access_token_password_reset
from schemas.buyers.buyerSchema import BuyerOut, UserSignUpIn
from schemas.vendors.vendorSchema import VendorOut
from utils.users.email import password_rest_email, account_purchased
from schemas.auth.authSchema import UpdatePassword, EmailReset,ResetPassword
from typing import Annotated, Union
import random




router = APIRouter(
    tags=["Users Auth"]
)




def generate_custom_id(prefix: str, n_digits: int) -> str:
    """Generate a custom ID with a given prefix and a certain number of random digits"""
    random_digits = ''.join([str(random.randint(0,9)) for i in range(n_digits)])
    return f"{prefix}{random_digits}"


"""
Users sign up route
"""


@router.post('/signup', status_code =status.HTTP_201_CREATED)
async def create_new_user(data : UserSignUpIn , db:Session=Depends(get_db)):
  # Check if the user already exists
  if db.query(UserSignUp).filter(UserSignUp.email == data.email).first():
    raise HTTPException(status_code=400, detail="Email is already in use")
  
  # Hash password before saving it to database
  data.password = hash(data.password)
    # Define buyer and vendor variables
  buyer = None
  vendor = None
  if data.user_type == "buyer":
    custom_id = generate_custom_id("BU",7)
    social_media_platform = ["none"]
    buyer = Buyers(buyer_id=custom_id, social_media_platform=social_media_platform, **data.dict())
  elif  data.user_type == "vendor":
    custom_id = generate_custom_id("VN",7)
    business_social_links = ["none"]
    vendor = Vendors(vendor_id=custom_id,business_social_links = business_social_links, **data.dict())
  else :
    raise HTTPException(status_code=400, detail="Pls select a corresponding user type")
  user = UserSignUp(user_id=custom_id, **data.dict())

  # Add user instances to the database session
  if buyer:
    db.add(buyer)
  if vendor:
    db.add(vendor)
  db.add(user)
  db.commit()
  db.refresh(user)
  await account_purchased("Registration Successful", data.email, {
  "title": "Sign up Successful",
  "name": data.full_name,
  
})

  return {"message": "Account Created Successfully"}






"""
User Login route

"""
@router.post('/login', response_model=dict)
def login(
    details: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Check if the login details belong to a user
    user = db.query(UserSignUp).filter(UserSignUp.email == details.username).first()
    if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # user_type = user.user_type

    # Create tokens based on user type
    access_token, refresh_token = create_tokens(user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "current_user": user.full_name,"user_type":user.user_type}





"""
To refresh token
"""

@router.post('/token/refresh', response_model=dict)
def refresh_token(
    refresh_token: str = Form(...),
    db: Session = Depends(get_db)
):
    token_data = verify_refresh_token(refresh_token)
    user_id = token_data.id
    email = token_data.email

    # Check if the token belongs to a user
    user = db.query(UserSignUp).filter(UserSignUp.user_id == user_id).first()
    # user_type = "buyer"
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    access_token, new_refresh_token = create_tokens(user)
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer", "current_user": user.full_name}




"""
To Update User's Password
"""
@router.put('/update-password')
async def update_password(
    password_data: UpdatePassword,
    current_user: Union[Buyers, Vendors] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify the current password
    if not verify(password_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password",
        )
    # Hash and update the new password
    hashed_password = hash(password_data.new_password)
    current_user.password = hashed_password

    # Commit the changes to the database
    db.commit()

    return {"message": "Password updated successfully"}



"""
To get current user
"""
@router.get('/current_user', response_model=Union[BuyerOut, VendorOut])
async def get_current_authenticated_user(current_user: Union[BuyerOut, VendorOut] = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with: me found")
    return  current_user



"""
User route
To reset Buyers password
"""

@router.post('/forgot_password')
async def password_reset(email: EmailReset, db: Session = Depends(get_db)):
    # Check if the email exists for a user
    user = db.query(Buyers).filter(Buyers.email == email.email).first()
    if user:
        user_type = "buyer"
    else:
        # If not a user, check if the email exists for a service provider
        vendor = db.query(Vendors).filter(Vendors.email == email.email).first()
        if vendor:
            user = vendor
            user_type = "vendor"
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found"
            )

    reset_token = create_password_reset_token(data={"email": user.email, "user_type": user_type})
    reset_link = f"http://localhost:5173/set_password/{reset_token}/"
    await password_rest_email("Password Reset", user.email,{
      "title": "Password Rest",
      "name": user.full_name,
      "reset_link": reset_link
    })
    
    return reset_link



"""
User route
To set new user's password
"""
@router.put('/set_password')
async def password(data: ResetPassword, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user_data = verify_access_token_password_reset(data.token, credentials_exception, db)
    user_email = user_data.email

    # Check if the email belongs to a user
    user = db.query(Buyers).filter(Buyers.email == user_email).first()
    if not user:
        # If not a user, check if the email belongs to a service provider
        vendor = db.query(Vendors).filter(Vendors.email == user_email).first()
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user = vendor

    # Update password
    user.password = hash(data.new_password)
    db.commit()
    return {"message": "Password reset successful"}
