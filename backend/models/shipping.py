from pydantic import BaseModel

class AddressRequest(BaseModel):
    src_address: str
    dest_address: str