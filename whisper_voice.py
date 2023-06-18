from whisper_cpp_python import Whisper
import time

whisper = Whisper(model_path="../whisper.cpp/models/ggml-small.bin", n_threads=3, strategy=1)

def transcribe(voice):
    start = time.time()
    output = whisper.transcribe(voice, language='ru')
    end = time.time()
    print('Time:', end-start)
    print('\n')
    print(output['text'])