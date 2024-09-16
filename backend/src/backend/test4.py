from pydantic import BaseModel
from datetime import datetime
import json

class AddressSource(BaseModel):
    original:str
    province:str
    province_code: str
    province_shortname: str
    city: str
    city_id: str
    city_code: str
    city_shortname: str
    county: str
    county_id: str
    county_code: str
    county_shortname: str
    town: str
    town_id: str
    town_code: str
    address: str

class Address(BaseModel):
    address:str
    city:str
    district:str
    province:str

class ShippingData(BaseModel):
    businessType:str
    consigedTime:str
    destAddress:Address
    searchPrice:str
    srcAddress:Address
    weight:int


json_string_src = '''{
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
}'''

json_string_dest = '''{
    "original": "广州市番禺区丽江花园华林居",
    "province": "广东省",
    "province_id": "5876",
    "province_code": "440000",
    "province_shortname": "广东",
    "city": "广州市",
    "city_id": "5911",
    "city_code": "440100",
    "city_shortname": "广州",
    "county": "番禺区",
    "county_id": "6091",
    "county_code": "440113",
    "county_shortname": "番禺",
    "town": "",
    "town_id": "",
    "town_code": "",
    "address": "丽江花园华林居"
}'''

src_data=AddressSource.model_validate_json(json_string_src)
dest_data=AddressSource.model_validate_json(json_string_dest)

shipping_data=ShippingData(
    businessType="2",
    consigedTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    destAddress=Address(
        address=dest_data.address,
        city=dest_data.city,
        district=dest_data.county,
        province=dest_data.province
    ),
    searchPrice="1",
    srcAddress=Address(
        address=src_data.address,
        city=src_data.city,
        district=src_data.county,
        province=src_data.province
    ),
    weight=1
)

final_json=shipping_data.model_dump_json(indent=2)

print(final_json)