import json
from pathlib import Path

def read_collection(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("资料文件必须是对象")
    return value
