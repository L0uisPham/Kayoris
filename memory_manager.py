
from uuid import uuid4
from time import time
from datetime import datetime
import json
import calendar
import os
import openai

def timestamp_to_string(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    
    year = dt_object.year
    month = calendar.month_name[dt_object.month]
    day = dt_object.day
    hour = dt_object.hour
    minute = dt_object.minute
    second = dt_object.second
    
    formatted_string = f"{month} {day}"
    
    return formatted_string

def save_metadata(metadata, unique_id):
    folder_path = "metadata"
    
    file_path = os.path.join(folder_path, f"{unique_id}.json")
    
    with open(file_path, "w", encoding='utf-8') as outfile:
        json.dump(metadata, outfile, ensure_ascii=False, sort_keys=True, indent=2)

def write_log(prompt, ai_response, unique_id):
    log_folder = 'logs'

    file_path = os.path.join(log_folder, unique_id + '.txt')
    
    with open(file_path, 'a') as file:
        file.write(prompt + '\n')
        file.write(ai_response + '\n')

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def load_conversations(results):
    tmp_results = []
    if 'matches' in results:
        for n in results['matches']:
            info = load_json('metadata/%s.json' % n['id'])
            tmp_results.append(info)
        ordered = sorted(tmp_results, key=lambda d: d['time'], reverse=False)
        messages = [i['message'] for i in ordered]
        return '\n'.join(messages).strip()
    else:
        return "No 'matches' key found in the results dictionary."

def gpt_embeddings(content, engine='text-embedding-ada-002'):
    content = content.encode(encoding='ASCII',errors='ignore').decode() # fix all unicode errors
    response = openai.Embedding.create(input=content,engine=engine)
    vector = response['data'][0]['embedding']
    return vector


def upload_metadata(user_input):
    payload = list()
    timestamp = time()
    timestring = timestamp_to_string(timestamp)
    unique_id = str(uuid4())
    metadata = {'speaker': 'Kayos', 'time': timestamp, 'message': 'Kayos: ' + user_input, 'timestring': timestring, 'uuid': unique_id}

    save_metadata(metadata, unique_id)
    embeddings = gpt_embeddings(user_input)
    payload.append((unique_id, embeddings))

