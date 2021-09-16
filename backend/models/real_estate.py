import orjson as orjson
from pydantic import BaseModel, Field

from utils import orjson_dumps
from models.enum import Region, Material


class RealEstate(BaseModel):
    class Config:
        use_enum_values = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        arbitrary_types_allowed = True

    region: Region
    material_type: Material
    total_area: float
    living_area: float
    kitchen_area: float
    floor_number: int
    total_floors: int
    year: int
    address: str
    underground: bool
    land: float = Field(required=False, default=None)
    lat: float = Field(required=False, default=None)
    lon: float = Field(required=False, default=None)
    AQI: int = Field(required=False, default=None)
    air_pollutant_concentration: dict = Field(required=False, default=None)
