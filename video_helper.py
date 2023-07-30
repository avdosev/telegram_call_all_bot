import uuid
import os
import io
import logging
from ffmpeg.asyncio import FFmpeg

# предварительная инициализация
os.makedirs('tmp', exist_ok=True)

async def video_to_audio(video: io.BytesIO):

    logging.info("starting to convert video...")

    video_tmp_filename = f'tmp/{uuid.uuid1()}'

    with open(video_tmp_filename, "wb") as f:
        f.write(video.getbuffer())

    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(video_tmp_filename)
        .output(
            "pipe:1",
            {"codec:a": "pcm_s16le"},
            vn=None,
            f="wav",
        )
    )
    
    try:
        audio = io.BytesIO(await ffmpeg.execute())
        logging.info("video converted")
    except:
        logging.info("video not converted")
    finally:
        os.remove(video_tmp_filename)
    
    return audio