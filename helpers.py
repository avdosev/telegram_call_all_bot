import json
import logging
import random
import re
from typing import Any, Optional, Sequence, Union

rnd = random.SystemRandom()


def read_json(path: str) -> dict[str, Any]:
    """Read JSON data from *path*.

    Returns an empty dictionary if the file does not exist.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def read_file(path: str) -> Optional[str]:
    """Return the contents of *path* or ``None`` if reading fails."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except OSError as exc:
        logging.error('cant read file %s: %s', path, exc)
        return None


def dump_json(path: str, obj: Any) -> None:
    """Write *obj* to *path* in JSON format."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def chat_data_path(chat_id: Union[int, str]) -> str:
    """Build path to JSON storage for a chat."""
    return f'data/{chat_id}.json'


# Backwards compatibility alias
p = chat_data_path


def get_groups(chat_id: Union[int, str]) -> dict[str, Any]:
    """Return groups stored for the given *chat_id*."""
    return read_json(chat_data_path(chat_id))


def add_groups(chat_id: Union[int, str], name: str, values: Sequence[str]) -> None:
    """Add or replace group *name* with *values* for *chat_id*."""
    path = chat_data_path(chat_id)
    g = read_json(path)
    g[name] = list(values)
    dump_json(path, g)


def del_group(chat_id: Union[int, str], name: str) -> None:
    """Delete group *name* for *chat_id* if it exists."""
    path = chat_data_path(chat_id)
    g = read_json(path)
    if name in g:
        del g[name]
        dump_json(path, g)


def random_bool(probability: float = 0.5) -> bool:
    """Return ``True`` with the given *probability*."""
    return rnd.random() > (1 - probability)


def indexes(iterable: Sequence[Any]) -> range:
    """Return index range for *iterable*."""
    return range(len(iterable))


_SENTENCE_SPLITTER = re.compile(r'(?<=[.!?])')


def split_text_to_chunks(text: str, max_length: int) -> list[str]:
    """Split *text* into chunks no longer than *max_length*."""
    sentences = _SENTENCE_SPLITTER.split(text)
    chunks: list[str] = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
