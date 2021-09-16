import enum


class Region(str, enum.Enum):
    Moscow = 'Moscow'
    SaintPetersburg = 'SaintPetersburg'


class Repair(str, enum.Enum):
    no_repair = 'no_repair'
    cosmetic = 'cosmetic'
    euro = 'euro'
    design = 'design'


class Material(str, enum.Enum):
    monolith = 'monolith'
    monolithBrick = 'monolithBrick'
    old = 'old'
    brick = 'brick'
    panel = 'panel'
    wood = 'wood'
    wireframe = 'wireframe'
    aerocreteBlock = 'aerocreteBlock'
    stalin = 'stalin'
    block = 'block'
    boards = 'boards'
    foamConcreteBlock = 'foamConcreteBlock'


class OfferType(str, enum.Enum):
    primary = 'primary'
    secondary = 'secondary'
    house = 'house'


