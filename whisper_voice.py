from whisper_cpp_python import Whisper
import concurrent.futures
import queue
import time
import asyncio
import logging

logger = logging.getLogger('whisper')

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='whisper')

whisper = Whisper(model_path="../whisper.cpp/models/ggml-small.bin", n_threads=4, strategy=1)
def transcribe_sync(voice, voice_id):
    start = time.time()
    output = whisper.transcribe(voice, language='ru')
    end = time.time()
    logger.info(f'Time: {end-start}, Id: {voice_id}')
    return output['text']


lock = asyncio.Lock()
async def transcribe(voice, *args):
    loop = asyncio.get_running_loop()
    async with lock:    
        return await loop.run_in_executor(executor, transcribe_sync, voice, *args)
