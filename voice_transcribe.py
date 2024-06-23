import whisper_fast_voice as whisper
from text_processing import fix_errors, split_to_paragraphs


async def transcribe(voice, *args) -> str:
    segments = await whisper.transcribe(voice, *args)
    text_segments = [segment.text for segment in segments]

    total_duration = segments[-1].end_time

    use_timecodes = total_duration > 1.1*60

    paragraphs = split_to_paragraphs(text_segments, segments if use_timecodes else None)
    
    fixed_text = fix_errors('\n\n'.join(paragraphs))
    
    return fixed_text
