import requests
import json


# Creating requests to primary, secondary properties and houses
payloads = [
    """
    {"jsonQuery":{"_type":"flatsale","room":{"type":"terms","value":[1,2,3,4,5,6,7,8,9]},"region":{"type":"terms","value":[1,2]},"engine_version":{"type":"term","value":2},"page":{"type":"term","value":PAGE_NUM},"building_status":{"type":"term","value":2}}} 
    """,
    """
    {"jsonQuery":{"region":{"type":"terms","value":[1,2]},"_type":"flatsale","engine_version":{"type":"term","value":2},"building_status":{"type":"term","value":1},"room":{"type":"terms","value":[1,2,3,4,5,6,7,8,9]},"page":{"type":"term","value":PAGE_NUM}}}
    """,
    """
    {"jsonQuery":{"region":{"type":"terms","value":[1,2]},"_type":"suburbansale","object_type":{"type":"terms","value":[1]},"engine_version":{"type":"term","value":2},"page":{"type":"term","value":PAGE_NUM}}}
    """,
]

API_URL = 'https://api.cian.ru/search-offers/v2/search-offers-desktop/'


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184'
}

COOKIES = {
    '_CIAN_GK':'9cccef26-b77f-4f9e-b12f-7e7fcb63a7cf',
    'adb':'1',
    'sopr_utm':'%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'first_visit_time':'1630680803663',
    'serp_stalker_banner':'1',
    'fingerprint':'c1fe3fb187cc7c7c3b2199d18734a318',
    'session_region_id':'1',
    'session_region_name':'%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'forever_region_id':'1',
    'forever_region_name':'%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'session_main_town_region_id':'1',
    'serp_registration_trigger_popup':'1',
    'is_push_declined':'true',
    'sopr_session':'65fce80de9d9425f',
    'cf_chl_2':'deba70539ce81e6',
    'cf_chl_prog':'a9',
    'cf_clearance':'PBS_bUanYfvn1jyq_5j3njSJiHEd8kT1KM02nMW_FUU-1631473490-0-150',
    '__cf_bm':'ZJz.nM6V1CKh1vXdIDsN5lWkEQdt2mP2QtIsMSlv_eg-1631473697-0-Advy1rVxoPpz35Ab6MQNKWRhxDSVX7p1RfLzEBql9zLsrdRDjEwlk0cVFR9wJ7oHj7tKX66UoG19b+125HK2FYo=',
}


# Creating JSON file
with open('data.json', 'r') as f:
    json_data = json.load(f)

# Releasing cash
existing_ads = set()
for key in json_data.keys():
    existing_ads.add(key)


# Parsing
# page_num == how much pages we want to parse
page_num = 1
while page_num < 200:
    for p in payloads:
        data = p.replace('PAGE_NUM', str(page_num))

        res = requests.post(API_URL, headers=HEADERS, cookies=COOKIES, data=data)

        out = res.json()

        if res.status_code != 200 or out['status'] != 'ok':
            print('> ERROR in:', data)
            continue
        else:
            print('> DONE!', data)

        new_count = 0
        for ad in out['data']['offersSerialized']:
            full_url = ad['fullUrl']
            if full_url in existing_ads:
                continue

            new_count += 1
            json_data[full_url] = ad

            existing_ads.add(full_url)

        print('Added new', new_count)

        with open('data.json', 'w') as f:
            json.dump(json_data, f)

    page_num += 1
