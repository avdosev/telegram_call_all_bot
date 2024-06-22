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
    
    segments = list(segments)
    text = split_voice_into_paragraphs(segments)
    
    end = time.time()
    
    logger.info(f'Time: {end-start}, Id: {file_id}')
    return text.strip()


lock = asyncio.Lock()
async def transcribe(voice, *args):
    loop = asyncio.get_running_loop()
    async with lock:    
        return await loop.run_in_executor(executor, transcribe_sync, voice, *args)


def split_voice_into_paragraphs(segments, threshold=1.0):
    paragraphs = []
    current_paragraph = []
    previous_time = None

    for segment in segments:
        time = segment.start
        if previous_time is not None and time - previous_time > threshold:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []

        current_paragraph.append(segment.text.strip())
        previous_time = segment.end

    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    paragraphs = merge_texts_on_condition(paragraphs)

    return '\n\n'.join(paragraphs)


def merge_texts_on_condition(texts):
    merged_text = []
    i = 0
    
    while i < len(texts):
        current_text = texts[i]
        
        # Проверяем, заканчивается ли текст на "..."
        if current_text.endswith("..."):
            # Если следующий текст существует, объединяем его с текущим
            if i + 1 < len(texts):
                current_text = current_text + " " + texts[i + 1]
                i += 1  # Пропускаем следующий текст, поскольку он уже объединён
        
        merged_text.append(current_text)
        i += 1
        
    return merged_text
