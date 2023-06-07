# 基于大语言模型的中文科技文献标注方法

这个仓库包含了我们论文的代码: 基于大语言模型的中文科技文献标注方法 - *A Chinese scientific literature annotation method based on large language model*。

## 中文科技领域实体标注数据集 ACSL

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
├── config.py        # 配置信息
├── dataset          # CSL 与 ACSL 数据集
├── handle_error.py  # 标注错误样本的处理
├── output           # 输出文件
├── process          # 数据处理
└── statistic        # 数据统计
```

## 基准测试

### 数据集

1. acsl: baseline/datasets/ACSL

### 模型

- `chinese-roberta-wwm-ext`: https://huggingface.co/hfl/chinese-roberta-wwm-ext

1. BERT+Softmax
2. BERT+CRF
3. BERT+Span

### 环境依赖

1. 1.1.0 =< PyTorch < 1.5.0
2. cuda=9.0
3. python3.6+

### 输入数据格式

```json
{"text_id":0,"text":"为了使联合收割机具有自动测产功能,提出了一种基于变权分层激活扩散的产量预测误差剔除模型,并使用单片机设计了联合收获机测产系统.测产系统的主要功能是:在田间进行作业时,收割机可以测出当前的运行速度,....","label":{"研究问题":{"联合收割机具有自动测产功能":[[3,15]]},"研究方法":{"基于变权分层激活扩散的产量预测误差剔除模型":[[22,42]]},"研究材料":{"单片机":[[47,49]],"霍尔传感器":[[118,122]],"电容压力传感器":[[124,130]],"ADC0804差分式A/D转换芯片":[[150,166]]},"研究成果":{"将系统应用在了收割机上,通过测试得到了谷物产量的测量值,并与真实值进行比较,验证了系统的可靠性":[[250,296]]}},"title":"谷物联合收获机自动测产系统设计-基于变权分层激活扩散模型","keywords":"联合收割机_测产系统_变权分层_激活扩散","subject":"农业工程","subject_area":"工学"}
```

### 代码运行方式
1. 进入 `baseline` 目录
1. 请修改 `run_ner_xxx.py` 或 `scripts/run_ner_xxx.sh` 中的配置信息。
2. 执行命令：`sh scripts/run_ner_xxx.sh`

**NOTE**: 预训练模型的目录结构

```text
├── model
|  └── bert_base
|  |  └── pytorch_model.bin
|  |  └── config.json
|  |  └── vocab.txt
|  |  └── ......
```

### ACSL上的基线模型测试结果

基准模型在 **dev** 上的性能:

**准确率 Precision (P):**
| 基线模型       | 问题   | 方法   | 评估度量 | 材料   | 成果   | 总体性能 |
|--------------|-------|-------|--------|-------|-------|--------|
| BERT+Softmax | 0.397 | 0.394 | 0.198  | 0.332 | 0.244 | 0.327  |
| BERT+CRF     | 0.421 | 0.415 | 0.207  | 0.355 | 0.253 | 0.344  |
| BERT+Span    | 0.492 | 0.471 | 0.305  | 0.415 | 0.309 | 0.413  |

**召回率 Recall (R):**
| 基线模型       | 问题   | 方法   | 评估度量 | 材料   | 成果   | 总体性能 |
|--------------|-------|-------|--------|-------|-------|--------|
| BERT+Softmax | 0.327 | 0.380 | 0.195  | 0.282 | 0.210 | 0.289  |
| BERT+CRF     | 0.357 | 0.408 | 0.216  | 0.319 | 0.235 | 0.319  |
| BERT+Span    | 0.331 | 0.387 | 0.157  | 0.278 | 0.185 | 0.282  |

**F1:**
| 基线模型       | 问题   | 方法   | 评估度量 | 材料   | 成果   | 总体性能 |
|--------------|-------|-------|--------|-------|-------|--------|
| BERT+Softmax | 0.359 | 0.387 | 0.196  | 0.305 | 0.226 | 0.307  |
| BERT+CRF     | 0.387 | 0.412 | 0.212  | 0.336 | 0.244 | 0.331  |
| BERT+Span    | 0.396 | 0.425 | 0.207  | 0.333 | 0.231 | 0.335  |

## 参考项目

- [Chinese Scientific Literature Dataset](https://github.com/ydli-ai/CSL)
- [Chinese NER using Bert](https://github.com/lonePatient/BERT-NER-Pytorch)
- [中文BERT-wwm](https://github.com/ymcui/Chinese-BERT-wwm)