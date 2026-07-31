# src/utils/file_io.py
import json

def load_json(file_path):
    """从 JSON 文件加载数据。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    """将数据保存为 JSON 文件。"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)