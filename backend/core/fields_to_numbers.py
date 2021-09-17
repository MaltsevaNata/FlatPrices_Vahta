from models import RealEstate

fields = {
    "region": {'Moscow': 1, 'SaintPetersburg': 2},

    "material_type": {'block': 0, 'brick': 1, 'monolith': 2, 'monolithBrick': 3, 'old': 4, 'panel': 5, 'stalin': 6,
                      'wireframe': 7}
}


def fields_to_numbers(data: RealEstate):
    data_dict = data.dict()
    for field in fields.keys():
        data_dict[field] = fields[field][data_dict[field]]
    print(data_dict)
    return data_dict


