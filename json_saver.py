"""
Module to save crawled data as human-readable JSON files.
"""

import json
import os
import datetime
import re


def save_json(url: str, text: str, topic: str):
    """
    Save the crawled data to a JSON file in the Jsons folder.
    Filename format: MM-DD-YYYY_HH-MM_sanitized_topic.json
    """
    os.makedirs("Jsons", exist_ok=True)

    current_time = datetime.datetime.now()
    date_str = current_time.strftime("%m-%d-%Y")
    time_str = current_time.strftime("%H-%M")
    sanitized_topic = topic.replace('/', '-').replace(' ', '_').replace(':', '-').replace('\\', '-')
    sanitized_topic = re.sub(r'[<>"\|\?\*]', '', sanitized_topic)
    sanitized_topic = re.sub(r'_+', '_', sanitized_topic).strip('_')
    filename = f"{date_str}_{time_str}_{sanitized_topic}.json"
    path = os.path.join("Jsons", filename)
    
    data = {
        "url": url,
        "text": text,
        "topic": topic,
        "timestamp": current_time.isoformat()
    }
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)