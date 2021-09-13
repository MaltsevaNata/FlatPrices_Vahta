import json
import csv


# Extracting major parameters from JSON data and transferring them to CSV
def converter(json_data, writer):
	for key in json_data:
		new_dict = {'key': key,
					'price': json_data[key]['bargainTerms']['price'],
					'total_area': json_data[key]['totalArea'],
					'living_area': json_data[key]['livingArea'],
					'kitchen_area': json_data[key]['kitchenArea'],
					'land': unittype_to_sqmt(json_data[key]['land']['area'], json_data[key]['land']['areaUnitType']) if json_data[key]['land'] else 0,
					'floor_number': json_data[key]['floorNumber'],
					'total_floors': json_data[key]['building']['floorsCount'],
					'year': json_data[key]['building']['deadline']['year'] if json_data[key]['building']['deadline'] else json_data[key]['building']['buildYear'],
					'bedrooms_number': json_data[key]['bedroomsCount'],
					'passenger_lifts_number': json_data[key]['building']['passengerLiftsCount'],
					'cargo_lifts_number': json_data[key]['building']['cargoLiftsCount'],
					'material_type': json_data[key]['building']['materialType'],
					'balconies_number': json_data[key]['balconiesCount'],
					'loggias_number': json_data[key]['loggiasCount'],
					'lng': json_data[key]['geo']['coordinates']['lng'],
					'lat': json_data[key]['geo']['coordinates']['lat'],
					'underground': bool_undeground(json_data[key]['geo']['undergrounds'])}
		writer.writerow(new_dict)

# Converting non-standart unit types into square meters
def unittype_to_sqmt(area, areaUnitType):
	if areaUnitType == 'sotka':
		return float(area) * 100
	elif areaUnitType == 'hectare':
		return float(area) * 10000
	else:
		print(areaUnitType)
		assert 0
	
# One of approaches to unify undeground data
def bool_undeground(undergrounds):
	if not undergrounds:
		return False

	for station in undergrounds:
		if station['time'] <= 15 and station['transportType'] == 'walk':
			return True

	return False


# Opening JSON, creating CSV and writing data to CSV
with open('data.json', 'r') as file:
	json_data = json.load(file)

with open('data.csv', 'w', newline='') as csvfile:
	columns = ['key', 'price', 'total_area', 'living_area', 'kitchen_area', 'land', 'floor_number', 'total_floors', 'year', 
				'bedrooms_number', 'passenger_lifts_number', 'cargo_lifts_number', 'material_type', 'balconies_number', 'loggias_number',
				'lng', 'lat', 'underground']
	writer = csv.DictWriter(csvfile, fieldnames=columns)
	writer.writeheader()
	converter(json_data, writer)