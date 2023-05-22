from utils import *

if __name__ == "__main__":
    
    with open("dataset/annotated_data/csl_camera_readly_filter.tsv", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        line = remove_extra_spaces(line)
        line = replace_chinese_punctuation(line)
        line = remove_special_chars(line)
        new_lines.append(line)
    
    with open("dataset/annotated_data/csl_camera_readly_filter_cleaned.tsv", 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    