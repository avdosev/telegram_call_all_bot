from whisper_cpp_python import Whisper
import concurrent.futures
import queue
import time
import asyncio

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='whisper')

whisper = Whisper(model_path="../whisper.cpp/models/ggml-small.bin", n_threads=4, strategy=1)
def transcribe_sync(voice):
    start = time.time()
    output = whisper.transcribe(voice, language='ru')
    end = time.time()
    print('Time:', end-start)
    print('\n')
    return output['text']


lock = asyncio.Lock()
async def transcribe(voice):
    loop = asyncio.get_running_loop()
    async with lock:    
        return await loop.run_in_executor(executor, transcribe_sync, voice)
