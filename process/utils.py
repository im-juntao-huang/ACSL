import re

def remove_extra_spaces(text):
    # 去除中文与中文之间的空白符
    text = re.sub(r'([\u4e00-\u9fa5]) +([\u4e00-\u9fa5])', r'\1\2', text)
    
    # 去除中文与英文之间的空白符
    text = re.sub(r'([\u4e00-\u9fa5]) +([a-zA-Z])', r'\1\2', text)
    text = re.sub(r'([a-zA-Z]) +([\u4e00-\u9fa5])', r'\1\2', text)
    
    # 保留英文之间的空白符
    text = re.sub(r'([a-zA-Z]) +([a-zA-Z])', r'\1 \2', text)
    
    # 去除数字和中文之间的空白符
    text = re.sub(r'([\u4e00-\u9fa5]) +(\d+)', r'\1\2', text)
    text = re.sub(r'(\d+) +([\u4e00-\u9fa5])', r'\1\2', text)
    
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


if __name__ == "__main__":
    # 示例用法
    input_text = "Hello   \t\t  World!\nThis   is  a   test."
    output_text = remove_extra_spaces(input_text)
    print(output_text)
    # 示例用法
    input_text = "你好，世界！这是一个测试：【OpenAI】"
    output_text = replace_chinese_punctuation(input_text)
    print(output_text)
      
    # 示例用法
    input_text = "Hello\ue466 World\ue011!\uf06c"
    output_text = remove_special_chars(input_text)
    print(output_text)