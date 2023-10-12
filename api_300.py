import time
import logging
import aiohttp
import asyncio
from helpers import read_file

logger = logging.getLogger(__name__)

endpoint = 'https://300.ya.ru/api/text-summary'
api_key = read_file('300_key')

async def get_summary(text) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint, 
                json={'text': text}, 
                headers={'Authorization': 'OAuth '+api_key, 'Content-Type': 'application/json'},
            ) as resp:
                res = await resp.json()
                print(f'status: {resp.status}, response: {res}')
    
        return '\n'.join('- '+ thesis for thesis in res['thesis'])
    except:
        return None


if __name__ == '__main__':
    async def main():
        text = 'Всё началось, когда я узнал про конкурс красоты кода от Сбера. Я как раз хотел поучаствовать в каком-нибудь эпичном конкурсе, а тут он мне и подвернулся, тем более что я - тот человек, которому есть что рассказать про красивый код. Я даже целую статью запилил о том, как писать красивый и понятный код. Так что я решил, что в данном случае мои шансы на победу - в отличие от остальных конкурсов - всё же больше нуля. Кроме того, я хотел выступить на конференции PiterPy (спойлер: хрен мне), чтобы рассказать там про красивый код и всё такое, поэтому участие в конкурсе и сравнение результатов было бы классным подспорьем.'
        print(await get_summary(text))

    asyncio.get_event_loop().run_until_complete(main())