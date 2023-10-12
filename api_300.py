import time
import logging
import aiohttp
from helpers import read_file

logger = logging.getLogger(__name__)

endpoint = 'https://300.ya.ru/api/text-summary'
api_key = read_file('300_key')

async def get_summary(text) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint, 
                data={'text': text}, 
                headers={'Authorization': api_key},
            ) as resp:
                res = await resp.json()
                logger.info(f'status: {resp.status}, response: {res}')
    
        return '\n'.join(res['thesis'])
    except:
        return None