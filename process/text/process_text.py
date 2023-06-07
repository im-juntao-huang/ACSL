import os
import re

def remove_extra_spaces(text):
    
    text = text.replace(" ", "")
    
    # 去除中文与中文之间的空白符
    # text = re.sub(r'([\u4e00-\u9fa5]) +([\u4e00-\u9fa5])', r'\1\2', text)
    
    # # 去除中文与英文之间的空白符
    # text = re.sub(r'([\u4e00-\u9fa5]) +([a-zA-Z])', r'\1\2', text)
    # text = re.sub(r'([a-zA-Z]) +([\u4e00-\u9fa5])', r'\1\2', text)
    
    # # 保留英文之间的空白符
    # text = re.sub(r'([a-zA-Z]) +([a-zA-Z])', r'\1 \2', text)
    
    # # 去除数字和中文之间的空白符
    # text = re.sub(r'([\u4e00-\u9fa5]) +(\d+)', r'\1\2', text)
    # text = re.sub(r'(\d+) +([\u4e00-\u9fa5])', r'\1\2', text)
    
    # 去除字符串前端的空格
    # text = text.lstrip()
    
    # # 去除 \t 后的所有空白符，并保留 \t
    # text = re.sub(r'\t +', '\t', text)
    
    # # 去除数字与英文之间的空白符
    # text = re.sub(r'([a-zA-Z]) +(\d+)', r'\1\2', text)
    # text = re.sub(r'(\d+) +([a-zA-Z])', r'\1\2', text)
    
    return text

def replace_chinese_punctuation(text):
    
    punctuation_map = {
        '。': '.', '，': ',', '！': '!', '？': '?', '；': ';', '：': ':', '“': '"', '”': '"',
        '‘': "'", '’': "'", '【': '[', '】': ']', '《': '<', '》': '>', '（': '(', '）': ')',
        '、': ',', '—': '-', '／': '/', '×': 'x',
    }
    
    chinese_punctuation = "".join(list(punctuation_map.keys()))
    english_punctuation = "".join(list(punctuation_map.values()))
    
    # 创建一个转换表格
    translation_table = str.maketrans(chinese_punctuation, english_punctuation)
    
    # 使用 translate() 方法替换标点符号
    text = text.translate(translation_table)
    
    return text

def remove_special_chars(text):
    special_chars = ['\ue466', '\ue00b', '\ue011', '\ue000', 
                     '\ue002', '\ue54f', '\u3000', '\ue025',
                     '\ue40a', '\ue024', '\ue44a', '\ue0c7',
                     '\ue1e4', '\ue2ea', '\uf06c', '\ue00c']
    
    for char in special_chars:
        text = text.replace(char, '')
    
    return text

def process_text(text):
    # 函数功能：去除多余空格、替换中文标点符号、去除特殊字符
    text = remove_extra_spaces(text)
    text = replace_chinese_punctuation(text)
    text = remove_special_chars(text)
    return text

if __name__ == "__main__":
    
    data_dir = "dataset/raw_data"
    
    with open(os.path.join(data_dir, "csl_camera_readly_filter.tsv"), 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        line = process_text(line)
        new_lines.append(line)
    
    with open(os.path.join(data_dir, "csl_camera_readly_filter_cleaned.tsv"), 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    