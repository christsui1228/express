import json
import time
import uuid
import requests
import hashlib
import base64
import urllib.parse
from pydantic import BaseModel, Field
from datetime import datetime

class Address(BaseModel):
    province: str
    city: str
    county: str
    address: str

class ShippingData(BaseModel):
    businessType: str
    consignedTime: str
    destAddress: Address
    searchPrice: str
    srcAddress: Address
    weight: float = Field(..., description="Weight of the package in kg")

# 顺丰 API 常量
partnerID = 'Y4E4GTVT'
checkword = 'UC5OG1vBK9WoDiHQLh1aEAp0gts3Qkxn'
reqURL = 'https://sfapi.sf-express.com/std/service'
serviceCode = "EXP_RECE_QUERY_DELIVERTM"

def call_sf_express_service(shipping_data: ShippingData):
    msgData = shipping_data.json()
    requestID = str(uuid.uuid1())
    timestamp = str(int(time.time()))

    try:
        encoded_msg_data = urllib.parse.quote_plus(msgData)
        str_to_sign = f"{encoded_msg_data}{timestamp}{checkword}"

        m = hashlib.md5()
        m.update(str_to_sign.encode('utf-8'))
        msgDigest = base64.b64encode(m.digest()).decode('utf-8')
        
        data = {
            "partnerID": partnerID,
            "requestID": requestID,
            "serviceCode": serviceCode,
            "timestamp": timestamp,
            "msgDigest": msgDigest,
            "msgData": msgData
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        res = requests.post(reqURL, data=data, headers=headers)
        res.raise_for_status()
        
        resp = res.json()
        if resp.get("apiResultCode") in ["A0000", "A1000"]:
            print("SF API call successful")
            return resp
        else:
            print(f"SF API Error: {resp}")
            return None
        
    except Exception as e:
        print(f"SF API call failed: {e}")
    
    return None