import os
from rave_python import Rave
from config.environ import settings


# rave = Rave({settings.rave_secret_key})
rave = Rave("FLWPUBK_TEST-8fcc600fd29c191729ceebe4f60028c9-X", "FLWSECK_TEST-4436a0a5400d628b2b6d68ebbf306514-X",usingEnv = False)
res = rave.VirtualAccount.create({
    "email": "developers@flutterwavego.com",
    "narration": "Payment for goods or services",
    "amount": 3000
})
print(res)