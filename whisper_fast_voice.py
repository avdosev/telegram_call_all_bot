from faster_whisper import WhisperModel
import concurrent.futures
import time
import asyncio
import logging

logger = logging.getLogger('whisper-fast')

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='whisper-faster')

model = WhisperModel('small', device="cpu", compute_type="int8")

def transcribe_sync(voice, file_id):
    start = time.time()
    segments, info = model.transcribe(voice, beam_size=5)

    logger.debug("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    text = ' '.join([segment.text for segment in segments if len(segment.text) > 0])
    
    end = time.time()
    
    logger.info(f'Time: {end-start}, Id: {file_id}')
    return text.strip()


lock = asyncio.Lock()
async def transcribe(voice, *args):
    loop = asyncio.get_running_loop()
    async with lock:    
        return await loop.run_in_executor(executor, transcribe_sync, voice, *args)
