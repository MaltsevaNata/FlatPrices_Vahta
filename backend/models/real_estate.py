
import orjson as orjson
from pydantic import BaseModel, Field

from utils import orjson_dumps
from models.enum import Region, Repair, OfferType, Material


class RealEstate(BaseModel):
    class Config:
        use_enum_values = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        arbitrary_types_allowed = True

    region: Region
    offer_type: OfferType
    repair: Repair
    material_type: Material
    total_area: float
    living_area: float
    kitchen_area: float
    year: float
    underground: bool
    land: float = Field(required=False, default=None)
