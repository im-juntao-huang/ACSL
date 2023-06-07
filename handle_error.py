import openai
import json
import os

from tqdm import tqdm
from chat_scie import read_data, get_prompt
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import *

openai.api_key = api_key_list[0] # 默认 api_key

# 异常样本处理
def process_error_sample(error_text_id, raw_data):

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": get_prompt(raw_data[error_text_id])}
        ],
        temperature=0.0,
    )

    # 保存样本
    try:        
        json_object = json.loads(result['choices'][0]['message']['content'])
        json_object['text'] = raw_data[error_text_id]
        json_object['text_id'] = error_text_id
    except Exception:
        print("==> 样本格式化失败，跳过...")
        print("==> LLM Result: ", result['choices'][0]['message']['content'])
        return None

    return json_object

if __name__ == '__main__':
    
    # 读取数据
    file_path = "dataset/raw_data/csl_camera_readly_filter_cleaned.tsv"
    raw_data = read_data(file_path)
    
    error_text_ids = [99905]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_error_sample, i, raw_data) for i in error_text_ids]
        
        # Create progress bar for futures
        with tqdm(total=len(futures)) as progress:
            for future in as_completed(futures):
                future.result()
                progress.update(1)

    add_json_objects = []
    for future in futures:
        if future.result() is not None:
            add_json_objects.append(future.result())
    
    with open("dataset/qa/qa_1_100000.json", 'r', encoding='utf8') as f:
        json_objects = json.load(f)
    
    json_objects.extend(add_json_objects)
    with open("dataset/qa/qa_1_100000.json", 'w', encoding='utf8') as f:
        json.dump(json_objects, f, ensure_ascii=False, indent=4)