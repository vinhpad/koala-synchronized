
import json
import requests
from config import KOALA_URL
from utils import (
    clear_table,
    formatted_date_time
)
from core.inout_core import (
    createCheckInOut
)
from tqdm import tqdm

async def getDataCheckInOut(token, page=1, start_time=0, end_time=1742988397):
    url = f'{KOALA_URL}/event/events?category=user&end={end_time}&page={page}&pass_type=1&start={start_time}&user_role=0&size=1000'
    payload = {}
    headers = {'Cookie': f'session={token}'}
    res = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(e)
        return {"total_page": 0, "current_page": page, "data": []}

async def checkInOut(timestamp, userEnrollNumber):
    try:
        # timestamp /= 1000
        timeStr = formatted_date_time(timestamp,"%Y-%m-%d %H:%M:%S")
        timeDate = formatted_date_time(timestamp, "%Y-%m-%d")
        originType = 'I'
        
        checkInOutData = (userEnrollNumber, timeStr, timeDate, originType)
        await createCheckInOut(checkInOutData)
    except Exception as error:
        print(f'Error | {error}')

async def syncCheckInOut(token, start_time, end_time):
    await clear_table("CheckInOut")
    try:
        init_data = await getDataCheckInOut(token)
        total_page = int(init_data['page']['total'])
        for page_id in tqdm(range(1, total_page+1)):
            data = await getDataCheckInOut(token, page_id, start_time, end_time)
            checkInOuts_info = data['data']
            
            for checkInOut_info in tqdm(checkInOuts_info):
                try:
                    timestamp = checkInOut_info['timestamp']
                    userEnrollNumber = checkInOut_info['subject']['id']
                    await checkInOut(timestamp, userEnrollNumber)
                except Exception as error:
                    print(f'Error | {error}')
    except Exception as error:
        print(f'Error | {error}')

