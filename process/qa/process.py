import json

def read_json(json_file):
    with open(json_file, 'r') as f:
        json_objects = json.load(f)
    return json_objects

def write_json(json_objects, json_file):
    with open(json_file, 'w') as f:
        json.dump(json_objects, f, indent=4, ensure_ascii=False)

# 查漏     
def check_missing_item(json_objects, start_idx, end_idx):
    
    ids = []
    for json_object in json_objects:
        for key, value in json_object.items():
            if key != 'text_id':
                continue
            else:
                ids += [value]
                break
                
    full_set = set(range(start_idx, end_idx))
    missing_list = list(full_set - set(ids))
    return missing_list

def sort_json_object_by_key(json_object, keys):
    # 函数功能：对 JSON 对象中的字段按照key的顺序进行排序
    
    # 1. 将 key 从 json_object 中 pop 出来
    pop_hub = {}
    for k in keys:
        pop_hub[k] = json_object.pop(k)
    # 2. 按照 key 的顺序重新添加到 json_object 中
    for key, value in pop_hub.items():
        json_object[key] = value
    # 3. 返回 json_object
    return json_object
    

def sort_json(json_objects, key='text_id'):
    sorted_json = sorted(json_objects, key=lambda x: x[key])
    return sorted_json

def main():
    start_idx = 0
    end_idx = 100000
    json_file = 'dataset/qa/qa_1_100000.json'
    json_objects = read_json(json_file)
    missing_list = check_missing_item(json_objects, start_idx, end_idx)
    print(missing_list)
    print(len(missing_list))
    
    for json_object in json_objects:
        sort_json_object_by_key(json_object, key=["text_id", "text", "answer"])
    
    json_objects = sort_json(json_objects)
    write_json(json_objects, json_file)
    
    
if __name__ == '__main__':
    main()