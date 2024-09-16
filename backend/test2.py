from pydantic import BaseModel
import json

class AddressInfo(BaseModel):
    province: str
    city: str
    county: str
    address: str
    
    class Config:
        extra = 'ignore'

# 原始 JSON 数据
json_data = {
    "original": "深圳市龙华新区观澜街道库坑新围村皇帝印工业区D栋",
    "province": "广东省",
    "city": "深圳市",
    "county": "龙华区",
    "address": "库坑新围村皇帝印工业区D栋"
}

# 使用 Pydantic 模型处理数据
address_info = AddressInfo.model_validate(json_data)

# 自定义编码函数
def custom_encoder(obj):
    if isinstance(obj, AddressInfo):
        return {
            "province": obj.province,
            "city": obj.city,
            "district": obj.county,  # 这里将 county 改为 district
            "address": obj.address
        }
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# 将处理后的数据转换为 JSON 字符串
json_output = json.dumps(address_info, default=custom_encoder, ensure_ascii=False)

print(json_output)

# 格式化输出
print(json.dumps(json.loads(json_output), indent=2, ensure_ascii=False))