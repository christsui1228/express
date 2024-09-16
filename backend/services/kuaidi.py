import http.client
import urllib
import hashlib
import time
import json
from pydantic import BaseModel
from typing import List, Optional

class AddressData(BaseModel):
    province: str
    city: str
    county: str
    address: str

    class Config:
        extra = 'ignore'

def process_address(address_str: str) -> Optional[AddressData]:
    conn = http.client.HTTPSConnection("kop.kuaidihelp.com")

    appId = '114703'
    method = 'cloud.address.cleanse'
    ts = int(time.time())
    appKey = '3d78be70c0f6187989aa6c2065f2282eec181c27'

    signStr = appId + method + str(ts) + appKey
    sign = hashlib.md5(signStr.encode('utf8')).hexdigest()

    payload_list = {
        'app_id': appId,
        'method': method,
        'ts': str(ts),
        'sign': sign,
        'data': json.dumps({
            "multimode": True,
            "address": address_str,
            "cleanTown": True
        })
    }
    
    payload = urllib.parse.urlencode(payload_list)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    try:
        conn.request("POST", "/api", payload, headers)
        res = conn.getresponse()
        data = res.read()

        response_json = json.loads(data.decode("utf-8"))
        
        if response_json.get('code') == 0 and response_json.get('data'):
            processed_address = response_json['data'][0]
            return AddressData(**processed_address)
        else:
            print(f"Error processing address: {response_json.get('msg')}")
            return None
        
    except Exception as e:
        print("Error occurred:", str(e))
        return None
    finally:
        conn.close()