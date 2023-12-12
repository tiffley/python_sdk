import json
import hashlib

def hash_dict(di: dict) -> hashlib.sha256:
    """
    convert dict to hash. Use this to check if 2 dicts are same
    """
    return hashlib.sha256(json.dumps(di, sort_keys=True).encode())


