import pandas as pd
import json

ENTITY_TYPES = ['研究问题', '研究方法', '评估度量', '研究材料', '研究成果']

# 统计每个学科下的每种实体类型的标注长度
data = []
with open('dataset/raw_data/csl_camera_readly_filter_cleaned.tsv', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            fields = line.split('\t')
            data.append(fields)

df = pd.DataFrame(data, columns=['title', 'content', 'keywords', 'subject', 'subject_area'])

# 读取文件，其中每一行是一个 json 对象
with open('dataset/raw_data/csl_camera_annotated_1_10000_result_fileter_format_cleaned.json', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    
# 判断 json 文件中的 text_id 字段是否对应 tsv 文件中的索引
for entity in data:
    text_id = entity['text_id']
    json_text = entity['text']
    tsv_text = df.iloc[text_id]['content']
    assert json_text == tsv_text

print('==> json 与 tsv 文件中的 text_id 字段对应')

# 统计每个学科下的每种实体类型的标注长度
subject_area_entity_type_length = {}
for subject_area in df['subject_area'].unique():
    if subject_area is None:
        print(subject_area)
    subject_area_entity_type_length[subject_area] = {}
    for entity_type in ENTITY_TYPES:
        subject_area_entity_type_length[subject_area][entity_type] = []

for entity in data:
    text_id = entity['text_id']
    label = entity['label']
    subject_area = df.iloc[text_id]['subject_area']
    for entity_type, entitys in label.items():
        for entity in entitys.keys():
            subject_area_entity_type_length[subject_area][entity_type].append(len(entity))

statistics = []
for subject_area in df['subject_area'].unique():
    for entity_type in ENTITY_TYPES:
        length_list = subject_area_entity_type_length[subject_area][entity_type]
        if len(length_list) == 0:
            mean_length = 0
        else:
            mean_length = sum(length_list) // len(length_list)
        statistics.append({'subject_area': subject_area, 'entity_type': entity_type, 'mean_length': mean_length})

df_statistics = pd.DataFrame(statistics)
pivot_table = df_statistics.pivot(index='subject_area', columns='entity_type', values='mean_length')

pivot_table.to_csv('statistic/length.csv', encoding='utf-8')             

# 统计每个学科下的每种实体类型的数量
counts = []
for subject_area in df['subject_area'].unique():
    for entity_type in ENTITY_TYPES:
        length_list = subject_area_entity_type_length[subject_area][entity_type]
        counts.append({'subject_area': subject_area, 'entity_type': entity_type, 'count': len(length_list)})

df_counts = pd.DataFrame(counts)
pivot_table = df_counts.pivot(index='subject_area', columns='entity_type', values='count')

pivot_table.to_csv('statistic/count.csv', encoding='utf-8')

# 统计每个学科下的样本数
subject_area_count = {}
for subject_area in df['subject_area'].unique():
    subject_area_count[subject_area] = 0

for entity in data:
    text_id = entity['text_id']
    subject_area = df.iloc[text_id]['subject_area']
    subject_area_count[subject_area] += 1

# 保存为 csv 文件
df_subject_area_count = pd.DataFrame(subject_area_count.items(), columns=['subject_area', 'count'])
df_subject_area_count.to_csv('statistic/subject_area_count.csv', encoding='utf-8')
    