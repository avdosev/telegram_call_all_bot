from faster_whisper import WhisperModel
import concurrent.futures
import time
import asyncio
import logging
from voice_segment import VoiceSegment

logger = logging.getLogger('whisper-fast')

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='whisper-faster')

model = WhisperModel('small', device="cpu", compute_type="int8")

def transcribe_sync(voice, file_id) -> list[VoiceSegment]:
    start = time.time()
    segments, info = model.transcribe(voice, beam_size=5)
    
    logger.debug("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    
    segments = [
        VoiceSegment(
            start_time=segment.start,
            end_time=segment.end,
            text=segment.text,
        ) 
        for segment in segments
    ]
    
    end = time.time()
    
    logger.info(f'Time: {end-start}, Id: {file_id}')
    return segments


lock = asyncio.Lock()
async def transcribe(voice, *args) -> list[VoiceSegment]:
    loop = asyncio.get_running_loop()
    async with lock:    
        return await loop.run_in_executor(executor, transcribe_sync, voice, *args)
