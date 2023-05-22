# 基于大语言模型的中文科技文献标注方法

这个仓库包含了我们论文的代码: 基于大语言模型的中文科技文献标注方法。

# 中文科技领域实体标注数据集 ACSL

由于 Github 文件大小限制，我们将数据集放在了 
- [Google Drive](https://drive.google.com/drive/folders/1e9aveXUsz6qe0C6MqdXR7-TyvxSzJvy_?usp=sharing)
- [百度网盘](https://pan.baidu.com/s/123rp_t6fCucMuz5iRXNMfQ?pwd=f0ie)
    -   提取码：f0ie

数据文件简介：
- `csl_camera_readly.tsv`: [中文科学文献数据集 CSL](https://github.com/ydli-ai/CSL)
- `csl_camera_readly_filter.tsv`: 过滤部分学科后的 CSL 数据集
- `csl_camera_readly_filter_cleaned.tsv`: 清洗后的 CSL 数据集
- `csl_camera_annotated_1_10000.json`: 基于大语言模型的原始标注数据集
- `csl_camera_annotated_1_10000_result_fileter_format_cleaned.json`: ACSL 数据集, 经过数据清洗后的数据集


使用方式：

- 将数据集放在 `dataset/raw_data` 文件夹下即可。

## 项目结构

```text
.
├── baseline # 基于 BERT 的基准测试模型
├── README.txt     
├── chat_scie.py     # 基于大语言模型的中文科技文献标注方法
├── dataset          # CSL 与 ACSL 数据集
├── handle_error.py  # 标注错误样本的处理
├── output           # 输出文件
├── process          # 数据处理
└── statistic        # 数据统计
```

## 参考项目

- [Chinese Scientific Literature Dataset](https://github.com/ydli-ai/CSL)
- [Chinese NER using Bert](https://github.com/lonePatient/BERT-NER-Pytorch)
- [中文BERT-wwm](https://github.com/ymcui/Chinese-BERT-wwm)