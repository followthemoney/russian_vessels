
from typing import Dict, List
import requests
from dotenv import load_dotenv; load_dotenv()
import json
import os
from pathlib import Path
import logging
import platform

GFW_API_KEY = os.environ.get('GFW_API_KEY')

if platform.system() == 'Linux':
    PATH_DATA= Path(os.environ.get('PATH_LIVESTOCK_UBUNTU'))
elif platform.system() == 'Darwin':
    PATH_DATA = Path(os.environ.get('PATH_LIVESTOCK'))

logging.basicConfig(level=logging.INFO, 
                    filename=PATH_DATA.joinpath('logs', 'russia.logs'), 
                    filemode='w', 
                    format=('%(asctime)s - %(levelname)s - %(message)s'))

def get_eez_list():
    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/datasets/public-eez-areas/context-layers'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}
    
    r = requests.get(ENDPOINT, headers=headers)
    result = r.json()
    
    return result 


def get_events_by_flag_and_geometry(flag: str,
                                    start_date: str,
                                    end_date: str,
                                    event_type: str,
                                    path_out: str,
                                    geometry: Dict  = None,
                                    region: Dict = None
                                    )-> Dict:

    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/events?'

    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}

    
    if event_type == 'encounter':
        dataset = 'public-global-encounters-events:latest'
    elif event_type == 'fishing': 
        dataset = 'public-global-fishing-events:latest'
    elif event_type == 'loitering':
        dataset = 'public-global-loitering-events:latest'
    elif event_type == 'port_visits':
        dataset = 'public-global-port-visits-c2-events:latest'
    elif event_type == 'ais':
        dataset = 'public-global-gaps-events:latest&gap-intentional-disabling=True'
    else:
        raise ValueError(f'Event type must be "encounter", "fishing", "loitering", "port_visits" or "ais" not {event_type}')

    url = f'limit=99999&offset=0'

    data = {"datasets": [ f"{dataset}" ],
            "startDate": f"{start_date}",
            "endDate": f"{end_date}",
            "flags": [ f"{flag}"],
            "vesselTypes": [ 'BUNKER','CARGO','DISCREPANCY','CARRIER','FISHING','GEAR','OTHER','PASSENGER','SEISMIC_VESSEL','SUPPORT' ]
            }
    
    if region is not None:
        data.update({'region': {'id': region,
                                'dataset': 'public-eez-areas'}})
    elif geometry is not None:
        data.update({'geometry': geometry})

    
    r = requests.post(ENDPOINT + url, headers=headers, data=json.dumps(data))

    if r.status_code == 200 or r.status_code==201:
        result = r.json()
        if result.get('total') > 0:
            with open(path_out, 'a') as file:
                file.write(f'{result}\n')
    
        return result

    elif r.status_code != 200: 
        print(r.text)               
        logging.error(f'Something went wrong --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    return None
    
def get_vessel_info(ids: List,
                    path_out: str)->List:
    
    ENDPOINT = 'https://gateway.api.globalfishingwatch.org/v3/vessels?datasets[0]=public-global-vessel-identity:latest&ids[0]='
    
    headers = {'Authorization': f"Bearer {GFW_API_KEY}",
               'Content-Type': 'application/json'}
    
    results = []
    for id in ids:
        try:
            r = requests.get(f"{ENDPOINT}{id}&registries-info-data=ALL", headers=headers)
        except: 
            continue
        if r.status_code == 200 or r.status_code == 201:
            result = r.json()
            if result.get('total') > 0:
                with open(path_out, 'a') as file:
                    file.write(f'{result}\n')
                results.append(result)
        elif r.status_code != 200 or r.status_code != 201:
             print(r.text)               
        logging.error(f'Something went wrong --> status code: {r.status_code} - reason: {r.reason}\nplease check')

    return results