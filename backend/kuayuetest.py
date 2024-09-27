import requests
import json
import time
import hashlib

class KyExpressAPI:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.token = None
        self.refresh_token = None
        self.token_expire_time = 0
        self.token_url = "https://open.ky-express.com/security/token"
        self.api_url = "https://open.ky-express.com/router/rest"

    def get_token(self):
        headers = {
            "Content-Type": "application/json",
            "X-from": "openapi_app"
        }
        data = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        response = requests.post(self.token_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if result['success']:
            self.token = result['data']['token']
            self.refresh_token = result['data']['refresh_token']
            self.token_expire_time = time.time() + result['data']['expire_time']
        else:
            raise Exception(f"Failed to get token: {result['msg']}")

    def ensure_valid_token(self):
        if not self.token or time.time() > self.token_expire_time - 60:  # Refresh 60 seconds before expiration
            self.get_token()

    def generate_md5_signature(self, timestamp, body):
        signature_string = f"{self.app_secret}{timestamp}{body}"
        return hashlib.md5(signature_string.encode()).hexdigest().upper()

    def call_api(self, method, biz_body):
        self.ensure_valid_token()

        timestamp = str(int(time.time() * 1000))
        body_json = json.dumps(biz_body, ensure_ascii=False)
        signature = self.generate_md5_signature(timestamp, body_json)

        headers = {
            "Content-Type": "application/json",
            "token": self.token,
            "sign": signature,
            "appkey": self.app_key,
            "method": method,
            "timestamp": timestamp,
            "format": "JSON"
        }

        response = requests.post(self.api_url, headers=headers, data=body_json.encode('utf-8'), timeout=(3, 15))
        response.raise_for_status()
        result = response.json()

        if result['code'] in [6000, 6001, 6002, 6003]:
            self.get_token()
            return self.call_api(method, biz_body)  # Retry with new token

        return result

    def call_multiple_apis(self, methods, biz_bodies):
        results = {}
        for method, biz_body in zip(methods, biz_bodies):
            try:
                result = self.call_api(method, biz_body)
                results[method] = result
            except Exception as e:
                results[method] = {"error": str(e)}
        return results

def main():
    app_key = "83417"  # 替换为您的沙盒环境app_key
    app_secret = "B7B18FA140F8ECFD8BCBDBE28724A24D"  # 替换为您的沙盒环境app_secret

    api = KyExpressAPI(app_key, app_secret)

    methods = [
        "open.api.openCommon.queryTimeliness",
        "open.api.openCommon.queryFreightCharge"
    ]
    
    biz_bodies = [
        {
            "customerCode": "02063137676",
            "mailingTime": "2024-09-24 10:00",
            "sendAddress": "广东省深圳市南山区西丽街道仙洞路16号深信服科技大厦",
            "collectAddress": "张子良 18211242431 广东省广州市白云区沙太路新百佳服装城 A21078  "
        },
        {
           "platformFlag": "E1MLIY94V1H9MYMO7ICH9TTFA24TKQHK",
           "customerCode": "02063137676",
           "beginAreaCode": "0755",
           "endAreaCode": "0711",
           "billingTime": "2024-09-2024 14:25",
           "pickupCustomerCode": "02063137676",
           "weight": 60,
           "unit": 1,
           "size": 2.2,
           "manageWeight": 13,
           "beginCityName": "深圳",
           "endCityName": "广州",
           "beginAddress": "2r15",
           "endAddress": "1p7e"
        }
    ]

    try:
        responses = api.call_multiple_apis(methods, biz_bodies)
        for method, response in responses.items():
            print(f"\nResponse for {method}:")
            print(json.dumps(response, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()