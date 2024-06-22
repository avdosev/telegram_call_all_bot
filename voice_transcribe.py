from transformers import pipeline
import whisper_fast_voice as whisper


error_fixing_pipe = pipeline("text2text-generation", model="ai-forever/FRED-T5-1.7B-spell-distilled-100m")


def fix_errors(text):
    paragraphs = text.split('\n\n')

    fixed_paragraphs = [error_fixing_pipe(paragpaph)[0]['generated_text'] for paragpaph in paragraphs]
    
    return '\n\n'.join(fixed_paragraphs)


async def transcribe(voice, *args) -> str:
    return fix_errors(await whisper.transcribe(voice, *args))
