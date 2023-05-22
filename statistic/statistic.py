import matplotlib.pyplot as plt
import seaborn as sns

# 支持中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.size'] = 14


# 统计学科
# 一级学科的论文数量以及占比
# 二级学科的论文数量以及占比
def count(lines):
    
    disciplines = {}
    subdisciplines = {}
    for line in lines:
        title, abstract, keyword, subdiscipline, discipline = line.strip().split('\t') # 题目, 摘要，关键词，二级学科，一级学科
        if discipline not in disciplines.keys():
            disciplines[discipline] = 0
        else:
            disciplines[discipline] += 1
            
        if subdiscipline not in subdisciplines.keys():
            subdisciplines[subdiscipline] = 0
        else:   
            subdisciplines[subdiscipline] += 1
    
    # 排序
    disciplines = dict(sorted(disciplines.items(), key=lambda x: x[1], reverse=True))
    subdisciplines = dict(sorted(subdisciplines.items(), key=lambda x: x[1], reverse=True))
    
    print("\n一级学科的论文数量以及占比")
    total = len(lines)
    for key, value in disciplines.items():
        print(key, value, round(value/total, 4))
    
    print("\n二级学科的论文数量以及占比")
    for key, value in subdisciplines.items():
        print(key, value, str(round(value/total* 100, 2) )+"%")
        
    print("\n一级学科数量：", len(disciplines.keys()))
    print("\n二级学科数量：", len(subdisciplines.keys()))
    
    return disciplines, subdisciplines


def filter_non_sci(lines: list) -> list:
    remain_discipline = ["工学", "理学", "农学", "医学"]
    filter_lines = []
    for line in lines:
        if line.strip().split('\t')[-1] in remain_discipline:
            filter_lines.append(line)
    
    return filter_lines


if __name__ == '__main__':
    
    file_path = 'dataset/raw_data/csl_camera_readly.tsv'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    lines = filter_non_sci(lines)
    with open("dataset/raw_data/csl_camera_readly_filter.tsv", 'w') as f:
        f.writelines(lines)
    print("总样本数：", len(lines))
    
    disciplines, subdisciplines = count(lines)
    
    # 画饼图 disciplines
    colors = sns.color_palette('pastel')
    plt.figure(figsize=(12, 12))
    plt.pie([float(v) for v in disciplines.values()], labels=[k for k in disciplines.keys()], autopct='%1.1f%%', colors=colors)
    plt.savefig('statistic/一级学科数量分布.png', dpi=300)
    
    # 画图 subdisciplines
    plt.figure(figsize=(12, 12))
    plt.pie([float(v) for v in subdisciplines.values()], labels=[k for k in subdisciplines.keys()], autopct='%1.1f%%', colors=colors)
    plt.savefig('statistic/二级学科数量分布.png', dpi=300)

        
