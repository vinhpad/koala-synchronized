import os
import json
import requests
import asyncio
from config import (
    KOALA_URL, 
    KOALA_USERNAME, 
    KOALA_PASSWORD
)
from service.inout_services import syncCheckInOut
from service.user_services import syncUserInfo

async def getToken():
    
    url = f'{KOALA_URL}/auth/login'
    
    payload = json.dumps({
        "username": KOALA_USERNAME,
        "password": KOALA_PASSWORD
    })
    headers = {
        'User-Agent': 'Koala Admin',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=5, stream=True)
        try:
            session = response.cookies.values()[0]
            print('Successfully logged in !')
            return session
        except:
            return False
    except Exception as error:
        print(f'Error | {error}')
        return False


async def main():
    token = await getToken()
    await syncCheckInOut(token, 0, 1842988397)
    await syncUserInfo(token)
if __name__ == "__main__":
    asyncio.run(main())