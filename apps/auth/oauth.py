from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.database import get_db
from schemas.auth.authSchema import TokenData,PasswordResetTokenData
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.allModels import Buyers, Vendors
from config.environ import settings



SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days
RESET_PASSWORD_TOKEN_EXPIRE_MINUTES = settings.reset_password_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')




def verify_access_token_password_reset(token: str, credentials_exception, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
        return PasswordResetTokenData(email=email)
    except JWTError:
        raise credentials_exception
    



def create_tokens(user, user_type):
    if user_type == "buyer":
        to_encode = {"buyer_id": user.buyer_id, "email": user.email}
    elif user_type == "vendor":
        to_encode = {"vendor_id": user.vendor_id, "email": user.email}
    else:
        raise ValueError("Invalid user type")

    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": access_expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    to_encode.update({"exp": refresh_expire})
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        buyer_id = payload.get("buyer_id")
        vendor_id = payload.get("vendor_id")
        email = payload.get("email")
        if buyer_id is None and vendor_id is None or email is None:
            raise JWTError
        if buyer_id:
            token_data = TokenData(id= buyer_id, email=email)
        elif vendor_id:
            token_data = TokenData(id=vendor_id, email=email)
        return token_data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        buyer_id = payload.get("buyer_id")
        vendor_id = payload.get("vendor_id")
        email = payload.get("email")
        if email is None:
            raise credentials_exception
        if buyer_id:
            user = db.query(Buyers).filter(Buyers.buyer_id == buyer_id).first()
        elif vendor_id:
            user = db.query(Vendors).filter(Vendors.vendor_id == vendor_id).first()
        else:
            raise credentials_exception
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def create_password_reset_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt