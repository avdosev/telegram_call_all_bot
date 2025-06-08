import asyncio
import concurrent.futures
from PIL import Image
import pytesseract
import io

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='ocr')


def ocr_sync(image_bytes: bytes) -> str:
    with Image.open(io.BytesIO(image_bytes)) as img:
        text = pytesseract.image_to_string(img, lang='rus+eng')
    return text.strip()

lock = asyncio.Lock()
async def ocr_image(image_bytes: bytes) -> str:
    loop = asyncio.get_running_loop()
    async with lock:
        return await loop.run_in_executor(executor, ocr_sync, image_bytes)
