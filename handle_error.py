import openai
import json
import os
from chat_scie import read_data, get_prompt

# 设置网络代理
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 异常样本处理
def process_error_sample(error_text_id, raw_data):

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": get_prompt(raw_data[error_text_id])}
        ],
        temperature=0.0,
    )

    print("LLM Result: ", result['choices'][0]['message']['content'])

    # 格式化输出
    print("==> 格式化输出...")
    print(result['choices'][0]['message']['content'] \
            .replace('```', '') \
            .replace('json', '') \
            .replace('\'', '') \
            .replace('\n', '') \
            .replace('问题y"', '问题y') \
            .replace(' ', '') \
            .replace('，', ',') \
            .replace('。', '').split("输出结果为：")[-1])
    
    # 保存样本        
    json_object = json.loads(result['choices'][0]['message']['content'] \
                                .replace('```', '') \
                                .replace('json', '') \
                                .replace('\'', '') \
                                .replace('\n', '') \
                                .replace('问题y"', '问题y') \
                                .replace(' ', '') \
                                .replace('，', ',') \
                                .replace('。', '').split("输出结果为：")[-1])
    
    json_object['text'] = raw_data[error_text_id]
    json_object['text_id'] = error_text_id

    return json_object

if __name__ == '__main__':
    
    # 读取数据
    file_path = "dataset/raw_data/csl_camera_readly_filter_cleaned.tsv"
    raw_data = read_data(file_path)
    
    error_text_id = 156
    
    json_object = process_error_sample(error_text_id, raw_data)
    
    with open(str(error_text_id) + ".json", 'w', encoding='utf8') as f:
        json.dump(json_object, f, ensure_ascii=False)