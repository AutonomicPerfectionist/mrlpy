from dataclasses import dataclass, fields
import json

cache = {}


def mrl_dataclass(cls):
    """
    This decorator marks the decorated class as a dataclass.
    It also adds the class to mrlpy's json deserializer class cache.
    This means it will be automatically deserialized from json into a new instance
    of a decorated class. Serializing is much easier and doesn't require the cache.
    """
    global cache
    c = dataclass(cls)
    c_fields = fields(c)
    field_names = frozenset(f.name for f in c_fields)
    cache[field_names] = c
    return c


def decode(d: dict):
    global cache

    # Fix double encoding
    if 'data' in d:
        new_data = []
        for obj in d['data']:
            o = loads(obj)
            if isinstance(o, str):
                try:
                    o = loads(o)
                except ValueError:
                    pass
            new_data.append(o)
        d['data'] = new_data
    if "class" in d:
        del d["class"]

    f_names = frozenset(d)
    if f_names in cache:
        return cache[f_names](**d)
    return d


def loads(s: str):
    return json.loads(s, object_hook=decode)
