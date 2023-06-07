
#包含当前文件的路径作为搜索路径
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('.')

from process import read_json, write_json, sort_json_object_by_key
from chat_scie import get_prompt


def main():
    
    qa_raw_file = 'dataset/qa/qa_0_100000.json'
    json_objects = read_json(qa_raw_file)
    
    for json_object in json_objects:
        json_object['prompt'] = get_prompt(json_object['text'], type='qa').replace(" ", "").replace("\n将回答格式化为JSON格式，形如：{\"answer\":\"\"\"研究问题\"\"\"}为了避免格式错误，JSON中的回答必须包含在\"\"\"中。", "")
        json_object.pop('text')
        json_object.pop('text_id')
        sort_json_object_by_key(json_object, keys=["prompt", "answer"])
    
    train_data = json_objects[:int(len(json_objects) * 0.8)]    
    dev_data = json_objects[int(len(json_objects) * 0.8):]
    
    train_file = 'dataset/qa/qa_train.json'
    dev_file = 'dataset/qa/qa_dev.json'
    write_json(train_data, train_file)
    write_json(dev_data, dev_file)
    
if __name__ == '__main__':
    main()