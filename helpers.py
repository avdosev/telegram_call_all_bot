import json


def read_json(path):
    try:
        with open(path, 'r',  encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


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
