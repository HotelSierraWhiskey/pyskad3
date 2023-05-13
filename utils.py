import tomllib
import os


def get_key(key_name: str, tomlfile_path: str) -> list:
    try:
        with open(tomlfile_path, 'rb') as f:
            keys = tomllib.load(f)
            try:
                return keys[key_name]
            except KeyError:
                raise Exception(f"Couldn't find key: {key_name}")
    except FileNotFoundError:
        raise Exception("Couldn't locate TOML file")
