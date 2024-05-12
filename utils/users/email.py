from fastapi_mail import  MessageSchema, FastMail
from config.email import conf



# Send Email for successful signup
async def successful_signup(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="accountSignup.html")


"""
Mail to the buyer for a successful order created
"""
async def order_created_buyer(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="orderCreatedBuyer.html")


"""
Message to the vendor after an order is created
"""
async def order_created_vendor_venduit(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="orderReceivedVendor.html")



"""
Message to the vendor after an order is created who is not on venduit
"""
async def order_created_vendor_nonVenduit(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="orderForNonVenduit.html")



# Send Mail to reset password
async def password_rest_email(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="password_reset.html")