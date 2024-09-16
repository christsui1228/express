from pydantic import BaseModel
from datetime import datetime
import json
import time
import uuid
import requests
import hashlib
import base64
import urllib.parse

# 定义常量
partnerID = 'Y4E4GTVT'
checkword = 'UC5OG1vBK9WoDiHQLh1aEAp0gts3Qkxn'
reqURL = 'https://sfapi.sf-express.com/std/service'
serviceCode = "EXP_RECE_QUERY_DELIVERTM"

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

def call_sf_express_service(shipping_data: ShippingData):
    msgData = shipping_data.model_dump_json()
    requestID = str(uuid.uuid1())
    timestamp = str(int(time.time()))  # 使用秒级时间戳

    try:
        # URL编码 msgData
        encoded_msg_data = urllib.parse.quote_plus(msgData)
        
        # 生成签名
        str_to_sign = f"{encoded_msg_data}{timestamp}{checkword}"
        print(f"String to sign: {str_to_sign}")  # 调试输出
        
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
        
        print(f"Request data: {data}")  # 调试输出
        
        res = requests.post(reqURL, data=data, headers=headers)
        res.raise_for_status()
        
        resp = res.json()
        if resp.get("apiResultCode") in ["A0000", "A1000"]:  # 考虑两种成功的情况
            print("API调用成功")
            return resp
        else:
            print(f"API Error: {resp}")
            return None
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
    except json.JSONDecodeError:
        print("Invalid JSON response from API")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

def main():
    # 示例数据
    src_address = Address(
        address="库坑新围村皇帝印工业区D栋",
        city="深圳市",
        district="龙华区",
        province="广东省"
    )
    
    dest_address = Address(
        address="丽江花园华林居",
        city="广州市",
        district="番禺区",
        province="广东省"
    )
    
    shipping_data = ShippingData(
        businessType="2",
        consignedTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        destAddress=dest_address,
        searchPrice="1",
        srcAddress=src_address,
        weight=1
    )

    # 调用顺丰 API
    result = call_sf_express_service(shipping_data)
    
    if result:
        print("API调用成功：")
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
        print("API调用失败")

if __name__ == "__main__":
    main()