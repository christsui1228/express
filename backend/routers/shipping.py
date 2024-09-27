from fastapi import APIRouter, HTTPException
from models.shipping import ShippingRequest  # 更新导入
from services.kuaidi import process_address
from services.sf_express import call_sf_express_service, ShippingData, Address
from datetime import datetime

router = APIRouter()

@router.post("/process_shipping")
async def process_shipping(request: ShippingRequest):  # 更新参数
    # 处理源地址和目的地址
    src_processed = process_address(request.src_address)
    dest_processed = process_address(request.dest_address)

    if not src_processed or not dest_processed:
        raise HTTPException(status_code=400, detail="Failed to process address")
    
    # 准备顺丰 API 所需的数据
    src_address = Address(**src_processed.model_dump())
    dest_address = Address(**dest_processed.model_dump())

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    shipping_data = ShippingData(
        businessType=" ",
        consignedTime=current_time,
        destAddress=dest_address,
        searchPrice="1",
        srcAddress=src_address,
        weight=request.weight  # 使用请求中的重量
    )

    # 调用顺丰 API
    result = call_sf_express_service(shipping_data)

    if not result:
        raise HTTPException(status_code=500, detail="SF API call failed")
    
    return result