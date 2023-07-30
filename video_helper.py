import uuid
import os
import io
import logging

# предварительная инициализация
os.makedirs('tmp', exist_ok=True)

async def video_to_audio(video: io.BytesIO):

    logging.info("starting to convert video...")

    video_tmp_filename = f'tmp/{uuid.uuid1()}'

    with open(video_tmp_filename, "wb") as f:
        f.write(video.getbuffer())

    from ffmpeg.asyncio import FFmpeg
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
        audio = await ffmpeg.execute()
        logging.info("video converted")
    finally:
        os.remove(video_tmp_filename)
        logging.info("video not converted")
    
    return audio