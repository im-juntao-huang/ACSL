import json
import os

import pandas as pd
from utils import *

def filter_entities(json_objs):
    # 函数功能：去除实体类型不在 keep_types 中的实体
    keep_types = ['研究问题', '研究方法', '评估度量', '研究材料', '研究成果']
    for json_obj in json_objs:
        filtered_entities = [entity_dict for entity_dict in json_obj["entities"] if entity_dict["type"] in keep_types]
        json_obj["entities"] = filtered_entities
    return json_objs

def process_text(json_objects):
    # 函数功能：去除多余空格、替换中文标点符号、去除特殊字符
    for json_object in json_objects:
        text = json_object['text']
        text = remove_extra_spaces(text)
        text = replace_chinese_punctuation(text)
        text = remove_special_chars(text)
        json_object['text'] = text

        # 遍历 entities['entity'] 字段并去除特殊字符
        for entity_dict in json_object['entities']:
            text = entity_dict['entity']
            if (text is None) or (len(text) == 0):
                continue
            text = remove_extra_spaces(text)
            text = replace_chinese_punctuation(text)
            text = remove_special_chars(text)
            entity_dict['entity'] = text

    return json_objects

def merge_json_obejct(json_objects):
    for i in range(len(json_objects)):
        if i == 0:
            continue
        json_objects[0] += json_objects[i]
    
    json_objects = json_objects[0]
    
    return json_objects

def sort_entities(json_object):
    
    """对实体进行排序
    对字段"entities"按照"研究问题"、"研究方法"、"研究材料"、"评估度量"、"研究成果"的顺序进行排序
    """
    
    entities = json_object['entities'] # entities 字典数组
    
    sort_order = ("研究问题", "研究方法", "研究材料", "评估度量", "研究成果")
    def custom_sort_key(item):
        field = item["type"]
        return sort_order.index(field) if field in sort_order else len(sort_order)
    
    json_object['entities'] = sorted(entities, key=custom_sort_key)
    
    return json_object

def sort_entities(json_object):
    """对字典中的字段进行排序
    对 JSON 对象中的字段按照 "text_id", "text", "entities" 的顺序进行排序
    """
    
    entities = json_object.pop('entities')
    text = json_object.pop('text')
    json_object['text'] = text
    json_object['entities'] = entities

def split_dataset(json_objects: list):
    # 函数功能：将数据集分割为训练集和验证集
    length = len(json_objects)
    train_json = json_objects[:int(length * 0.8)]
    val_json =  json_objects[int(length * 0.8):]
    return (train_json, val_json)

def format_json_to_single_line(json_objects: list):
    # 函数功能：将 JSON 对象转换为单行字符串
    json_str_list = []
    for json_obejct in json_objects:
        json_str_list += [json.dumps(json_obejct, separators=(',', ':'), ensure_ascii=False)]
    
    return json_str_list

def generate_index_start_end(json_objects: list):
    # 循环处理每一组数据
    for json_obj in json_objects:
        entities = json_obj['entities']
        text = json_obj['text']
        for entity_dict in entities:
            entity_value = entity_dict['entity']
            if entity_value is not None:
                start_idx = text.find(entity_value)  # 查找实体值在文本中的起始位置
                end_idx = start_idx + len(entity_value) - 1  # 计算实体值在文本中的结束位置
                entity_dict['start_idx'] = start_idx
                entity_dict['end_idx'] = end_idx
                
    return json_objects

def remove_unfound(json_objects: list):
    # 函数的功能： 删除未找到的实体
    # 找到 start_idx 值为 -1 的字典并从 entities 中删除
    for json_object in json_objects:
        entities = json_object['entities']
        new_entities = []
        for entity in entities:
            if 'start_idx' not in entity or entity['start_idx'] == -1:
                continue
            new_entities.append(entity)
        json_object['entities'] = new_entities
    return json_objects
              
def convert_format(json_objects: list):
    new_json_objects = []
    for d in json_objects:
        new_d = {}
        new_d['text_id'] = d['text_id']
        new_d['text'] = d['text']
        new_d['label'] = {}
        for entity in d['entities']:
            if entity['entity'] is not None:
                if entity['type'] not in new_d['label']:
                    new_d['label'][entity['type']] = {}
                if entity['entity'] not in new_d['label'][entity['type']]:
                    new_d['label'][entity['type']][entity['entity']] = []
                new_d['label'][entity['type']][entity['entity']].append([entity['start_idx'], entity['end_idx']])
        new_json_objects.append(new_d)
    
    return new_json_objects

def add_fields(json_objects, source_tsv_file, field_names=['title', 'keywords', 'subject', 'subject_area']):
    # 读取tsv文件，数据类型为 DataFrame
    # 列名为 ['title', 'content', 'keywords', 'subject', 'subject_area']
    data = []
    with open(source_tsv_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                fields = line.split('\t')
                data.append(fields)

    df = pd.DataFrame(data, columns=['title', 'content', 'keywords', 'subject', 'subject_area'])
    
    # 函数功能：增加字段: title, keywords, subject, subject_area
    for idx, json_object in enumerate(json_objects):
        assert json_object['text'] == df.iloc[idx]['content'], f"NOT MATCH {json_object['text'][:10]}"
        for field in field_names:
            json_object[field] = df.iloc[idx][field]
    
    return json_objects

def save_to_json(json_objects, save_to_file, data_dir = "dataset"):
    
    # 将 JSON 对象转换为单行字符串
    json_str_list = format_json_to_single_line(json_objects)
    
    # 保存到文件
    with open(os.path.join(data_dir, save_to_file), 'w', encoding='utf-8') as f:
        f.writelines(line + '\n' for line in json_str_list)

    
if __name__ == '__main__':
    
    json_objects = json.load(open("dataset/annotated_data/csl_camera_annotated_1_10000.json", 'r', encoding='utf-8'))
    
    # 过滤不需要的标签
    json_objects = filter_entities(json_objects)
    # 处理文本：去除多余空格、替换中文标点符号、去除特殊字符
    json_objects = process_text(json_objects)
    # 生成索引
    json_objects = generate_index_start_end(json_objects)
    json_objects = remove_unfound(json_objects)
    # 转换格式
    json_objects = convert_format(json_objects)
    # 增加字段: title, keywords, subject, subject_area
    json_objects = add_fields(json_objects, source_tsv_file="dataset/annotated_data/csl_camera_readly_filter_cleaned.tsv")
    
    save_to_json(json_objects, save_to_file="csl_camera_annotated_1_10000_result_fileter_format_cleaned.json", data_dir="dataset/annotated_data")
    
    # 分割数据集
    train_json, val_json = split_dataset(json_objects)
    save_files = ['train.json', 'dev.json']
    
    for idx, json_objects in enumerate([train_json, val_json]):
        save_to_json(json_objects, save_to_file=save_files[idx], data_dir="dataset")
    
    
    
  
        