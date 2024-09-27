from pydantic import BaseModel, Field

class ShippingRequest(BaseModel):
    src_address: str
    dest_address: str
    weight: float = Field(..., gt=0, description="Weight of the package in kg")