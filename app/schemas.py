from typing import List
from pydantic import BaseModel
from bson.objectid import ObjectId


from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str


class StudentBaseSchema(BaseModel):
    name: str
    age: int
    address: Address    

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class StudentResponse(BaseModel):
    id: str

class StudentListResponseData(BaseModel):
    name: str
    age: int
    
class StudentListResponse(BaseModel):
    data: List[StudentListResponseData]