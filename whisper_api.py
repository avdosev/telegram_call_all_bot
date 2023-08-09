import uuid
import os
import time
import logging
from ffmpeg.asyncio import FFmpeg
import aiohttp
import asyncio

# предварительная инициализация
os.makedirs('tmp', exist_ok=True)
logger = logging.getLogger(__name__)

lock = asyncio.Lock()

async def transcribe(voice, *args):
    async with lock:   
        return await transcribe_api(voice, *args)

async def transcribe_api(voice, file_id): 
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        temp_filename = f'tmp/{uuid.uuid1()}'


        ffmpeg = (
            FFmpeg()
            .option("y")
            .input("pipe:0")
            .output(
                temp_filename,
                {"codec:a": "pcm_s16le"},
                vn=None,
                ar='16000',
                f="wav",
            )
        )


        await ffmpeg.execute(voice.getbuffer())
    
        data = aiohttp.FormData()
        with open(temp_filename, 'rb') as f:
            data.add_field('file',
                        f.read(),
                        filename='audio.wav')
        
        os.remove(temp_filename)

        async with session.post('http://0.0.0.0:8080/transcribe', data=data) as resp:
            res = await resp.json()
            logger.info(f'status: {resp.status}, response: {res}')

    end = time.time()
    logger.info(f'Time: {end-start}, Id: {file_id}')
            
    return res['result']