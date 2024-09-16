from pydantic import BaseModel, Field,ConfigDict

class AddressInfo(BaseModel):
    province: str
    city: str
    district: str = Field(alias="county")
    address: str
    
    model_config=ConfigDict(
        extra = 'ignore',
        populate_by_name = True,
        alias_generator=None
    )

# 使用示例
json_data = {
    "original": "深圳市龙华新区观澜街道库坑新围村皇帝印工业区D栋",
    "province": "广东省",
    "province_id": "5876",
    "province_code": "440000",
    "province_shortname": "广东",
    "city": "深圳市",
    "city_id": "5947",
    "city_code": "440300",
    "city_shortname": "深圳",
    "county": "龙华区",
    "county_id": "882409",
    "county_code": "460106",
    "county_shortname": "龙华",
    "town": "观澜街道",
    "town_id": "906263",
    "town_code": "",
    "address": "库坑新围村皇帝印工业区D栋"
}

address_info = AddressInfo.model_validate(json_data)
print(address_info.model_dump())