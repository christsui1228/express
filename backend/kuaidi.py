import http.client
import urllib
import hashlib
import time
import json
from pydantic import BaseModel, Field
from typing import List, Optional

class AddressData(BaseModel):
    province: str
    city: str
    county: str
    address: str

    class Config:
        extra = 'ignore'

class APIResponse(BaseModel):
    code: int
    msg: str
    data: Optional[List[AddressData]]

    class Config:
        extra = 'ignore'

# 自定义编码函数
def custom_encoder(obj):
    if isinstance(obj, AddressData):
        return {
            "province": obj.province,
            "city": obj.city,
            "district": obj.county,  # 这里将 county 改为 district
            "address": obj.address
        }
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def make_request():
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
            "address": "梦雪 15239867163 河南省 三门峡市 湖滨区 虢国路上阳路交叉口向东一百米路北诗美诗格美容院",
            "cleanTown": True
        })
    }

    payload = urllib.parse.urlencode(payload_list)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    print("Request URL: /api")
    print("Request Method: POST")
    print("Request Headers:", headers)
    print("Request Payload:", payload)

    try:
        conn.request("POST", "/api", payload, headers)
        res = conn.getresponse()
        data = res.read()

        print("Response Status:", res.status)
        print("Response Headers:", res.getheaders())
        print("Response Body:", data.decode("utf-8"))

        response_json = json.loads(data.decode("utf-8"))
        api_response = APIResponse(**response_json)
        
        if api_response.code == 0 and api_response.data:
            for address in api_response.data:
                # 使用自定义编码器转换数据
                json_output = json.dumps(address, default=custom_encoder, ensure_ascii=False)
                print("Processed Address:")
                print(json_output)
        else:
            print(f"Error: {api_response.msg}")

    except Exception as e:
        print("Error occurred:", str(e))
    finally:
        conn.close()

if __name__ == "__main__":
    make_request()