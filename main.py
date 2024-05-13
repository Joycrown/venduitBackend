from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from config.database import  get_db
from apps.auth import buyerMain, auth, vendorMain
from apps.products import Order
from fastapi.staticfiles import StaticFiles




app = FastAPI()


origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["Content-Length"],
  max_age=600,
)

app.include_router(buyerMain.router)
app.include_router(auth.router)
app.include_router(vendorMain.router)
app.include_router(Order.router)
# app.include_router(serviceProAuth.router)
# app.include_router(orderMain.router)
# app.include_router(quote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/testing')
def test_db(db: Session = Depends(get_db)):
  # user= db.query(Users).all()
  return {"message": "Database is connected"}


# Static file configuration
app.mount("/static", StaticFiles(directory="static"), name="static")