import http.client
import urllib
import hashlib
import time
import json
import uuid
import requests
import base64
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Kuaidi100 相关类和函数
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

def custom_encoder(obj):
    if isinstance(obj, AddressData):
        return {
            "province": obj.province,
            "city": obj.city,
            "district": obj.county,
            "address": obj.address
        }
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def process_address(address_str):
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
        api_response = APIResponse(**response_json)
        
        if api_response.code == 0 and api_response.data:
            return json.loads(json.dumps(api_response.data[0], default=custom_encoder, ensure_ascii=False))
        else:
            print(f"Error processing address: {api_response.msg}")
            return None

    except Exception as e:
        print("Error occurred:", str(e))
        return None
    finally:
        conn.close()

# 顺丰 API 相关类和函数
class Address(BaseModel):
    address: str
    city: str
    district: str
    province: str

class ShippingData(BaseModel):
    businessType: str
    consignedTime: str
    destAddress: Address
    searchPrice: str
    srcAddress: Address
    weight: int

# 顺丰 API 常量
partnerID = 'Y4E4GTVT'
checkword = 'UC5OG1vBK9WoDiHQLh1aEAp0gts3Qkxn'
reqURL = 'https://sfapi.sf-express.com/std/service'
serviceCode = "EXP_RECE_QUERY_DELIVERTM"

def call_sf_express_service(shipping_data: ShippingData):
    msgData = shipping_data.model_dump_json()
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

def main():
    # 处理源地址和目的地址
    src_address_str = "梦雪 15239867163 河南省 三门峡市 湖滨区 虢国路上阳路交叉口向东一百米路北诗美诗格美容院"
    dest_address_str = "张三 13800138000 广东省广州市番禺区丽江花园华林居"
    
    src_processed = process_address(src_address_str)
    dest_processed = process_address(dest_address_str)
    
    if src_processed and dest_processed:
        # 准备顺丰 API 所需的数据
        src_address = Address(**src_processed)
        dest_address = Address(**dest_processed)
        
        shipping_data = ShippingData(
            businessType=" ",
            consignedTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            destAddress=dest_address,
            searchPrice="1",
            srcAddress=src_address,
            weight=1
        )

        # 调用顺丰 API
        result = call_sf_express_service(shipping_data)
        
        if result:
            print("SF API call successful:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 解析并打印具体的配送信息
            api_result_data = json.loads(result['apiResultData'])
            deliver_tm_dto = api_result_data['msgData']['deliverTmDto']
            
            print("\n配送选项：")
            for option in deliver_tm_dto:
                print(f"业务类型: {option['businessTypeDesc']}")
                print(f"预计送达时间: {option['deliverTime']}")
                print(f"费用: {option['fee']} {option['currency']}")
                print("---")
        else:
            print("SF API call failed")
    else:
        print("Failed to process addresses")

if __name__ == "__main__":
    main()