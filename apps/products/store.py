from fastapi import  Depends,HTTPException,status,APIRouter, UploadFile,Query
from config.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.allModels import Vendors, UserSignUp, Store, Product
from apps.auth.auth import get_current_user
from schemas.products.productStoreSchema import StoreOut, ProductIn, ProductOut
from typing import Optional, List, Union


router= APIRouter(
  tags=["Vendor Store"]
)



"""
to get a vendor store

"""


@router.get('/vendor_store', status_code=status.HTTP_200_OK, response_model=StoreOut)
async def vendor_store (db: Session = Depends(get_db), current_user: Vendors = Depends(get_current_user) ):
  try:
    store = db.query(Store).filter(Store.vendor_id== current_user.vendor_id).first()
    return store
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
  
  
""""
to create product to store

"""""

@router.post("/store/create_products", response_model=ProductOut)
def create_product(product: ProductIn, db: Session = Depends(get_db),current_user: Vendors = Depends(get_current_user)):
  try:
    store = db.query(Store).filter(Store.store_name == current_user.store_name).first()
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    db_product = Product(store_name=store.store_name,**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    store.product_id = db_product.id
    db.commit()
    db.refresh(db_product)
    return db_product
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
  





"""
to get a product from store

"""


@router.get('/store/find_product', status_code=status.HTTP_200_OK, response_model=Union[ProductOut, List[ProductOut]])
async def find_product_from_store (search: Optional[str] = Query(None, title="Search product by name"), db: Session = Depends(get_db), current_user: Vendors = Depends(get_current_user) ):
  try:
    store = db.query(Store).filter(Store.vendor_id== current_user.vendor_id).first()
    if not store:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vendor has no store")
    print(store.store_name)
    if search :
      find_product= db.query(Product).filter(and_(Product.store_name==store.store_name,Product.product_name.ilike(f"%{search}%"))).first()
      if not find_product:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No {search} in store")
    else:
      find_product = db.query(Product).filter(Product.store_name==store.store_name).all()
      if not find_product:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No product in store")
    return find_product
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 