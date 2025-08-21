import asyncio
import concurrent.futures
import io

from PIL import Image
import pytesseract

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="ocr")


def ocr_sync(image_bytes: bytes) -> str:
    """Run OCR on *image_bytes* synchronously."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        text = pytesseract.image_to_string(img, lang="rus+eng")
    return text.strip()


lock = asyncio.Lock()


async def ocr_image(image_bytes: bytes) -> str:
    """Run OCR on *image_bytes* in a thread executor."""
    loop = asyncio.get_running_loop()
    async with lock:
        return await loop.run_in_executor(executor, ocr_sync, image_bytes)
