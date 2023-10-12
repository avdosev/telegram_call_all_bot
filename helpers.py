import json
import random
import re
import logging

rnd = random.SystemRandom()

def read_json(path):
    try:
        with open(path, 'r',  encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        logging.error('cant read file', path)
    
    return None


def dump_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.flush()


def p(chat_id): return f'data/{chat_id}.json'


def get_groups(chat_id):
    return read_json(p(chat_id))


def add_groups(chat_id, name, values):
    path = p(chat_id)
    g = read_json(path)
    g[name] = values
    dump_json(path, g)


def random_bool(probability=0.5):
    return rnd.random() > (1-probability)

def indexes(iterable):
    return range(len(iterable))

sentence_re_splitter = re.compile(r'(?<=[.!?])')
def split_text_to_chunks(text: str, max_length) -> list[str]:
    sentences = sentence_re_splitter.split(text)
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    
    # Добавляем последний оставшийся чанк, если есть
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

if "__main__" == __name__:
    text = "Это пример текста. Он содержит несколько предложений. Мы будем использовать этот текст для тестирования функции."
    max_length = 300
    chunks = split_text_to_chunks(text, max_length)

    for chunk in chunks:
        print(chunk)
