import asyncio
import json
import random

import requests

from config import KOALA_URL
from core.department_core import getDeptByDeptCode
from core.user_core import createUser
from utils import clear_table, formatted_date_time
from tqdm import tqdm

async def getDataSubject(token, page):
    
    url = f'{KOALA_URL}/subject/list?category=employee&size=1000'
    
    payload = {}
    
    headers = {'Cookie': f'session={token}'}

    data = []

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
    except Exception as error:
        print(f'Error : {error}')
    
    return data
        

async def syncUserInfo(token):
    try:
        await clear_table('UserInfo')
        init_data = await getDataSubject(token, 1)
        total_page = init_data['page']['total']
        for page_id in range(1, total_page+ 1):
            try:
                checkinout_raw_data = await getDataSubject(token, page_id)
                
                for raw_data in tqdm(checkinout_raw_data['data']):
                    try:
                        user_hire_day_timestamp = int(raw_data['create_time'])
                        user_hire_day_str = formatted_date_time(user_hire_day_timestamp, "%Y-%m-%d")

                        try:
                            user_group_id = str(raw_data['department'])
                            user_idd = await getDeptByDeptCode(user_group_id)
                        except:
                            user_idd = str(1)
                    
                        user_info = (
                            raw_data['id'],
                            raw_data['job_number'],
                            raw_data['name'],
                            raw_data['name'],
                            user_hire_day_str,
                            1,
                            True,
                            user_idd,
                            1
                        )
                        # print(user_info)
                        await createUser(user_info)
                    except Exception as error:
                        print(f'Error | {error}')
            except Exception as error:
                print(f'Error | {error}')
    except Exception as error:
        print(f'Error | {error}')
        