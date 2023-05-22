## BERT-based baseline models

BERT-based baseline models

### dataset list

1. acsl: datasets/ACSL

### model list

- chinese-roberta-wwm-ext: https://huggingface.co/hfl/chinese-roberta-wwm-ext

1. BERT+Softmax
2. BERT+CRF
3. BERT+Span

### requirement

1. 1.1.0 =< PyTorch < 1.5.0
2. cuda=9.0
3. python3.6+

### input format

```json
{"text_id":0,"text":"为了使联合收割机具有自动测产功能,提出了一种基于变权分层激活扩散的产量预测误差剔除模型,并使用单片机设计了联合收获机测产系统.测产系统的主要功能是:在田间进行作业时,收割机可以测出当前的运行速度,....","label":{"研究问题":{"联合收割机具有自动测产功能":[[3,15]]},"研究方法":{"基于变权分层激活扩散的产量预测误差剔除模型":[[22,42]]},"研究材料":{"单片机":[[47,49]],"霍尔传感器":[[118,122]],"电容压力传感器":[[124,130]],"ADC0804差分式A/D转换芯片":[[150,166]]},"研究成果":{"将系统应用在了收割机上,通过测试得到了谷物产量的测量值,并与真实值进行比较,验证了系统的可靠性":[[250,296]]}},"title":"谷物联合收获机自动测产系统设计-基于变权分层激活扩散模型","keywords":"联合收割机_测产系统_变权分层_激活扩散","subject":"农业工程","subject_area":"工学"}
```

### run the code

1. Modify the configuration information in `run_ner_xxx.py` or `run_ner_xxx.sh` .
2. `sh scripts/run_ner_xxx.sh`

**note**: file structure of the model

```text
├── model
|  └── bert_base
|  |  └── pytorch_model.bin
|  |  └── config.json
|  |  └── vocab.txt
|  |  └── ......
```

### the result of baseline models on ACSL

The overall performance of baseline models on **dev**:

**Precision (P):**
| 基线模型       | 问题   | 方法   | 评估度量 | 材料   | 成果   | 总体性能 |
|--------------|-------|-------|--------|-------|-------|--------|
| BERT+Softmax | 0.397 | 0.394 | 0.198  | 0.332 | 0.244 | 0.327  |
| BERT+CRF     | 0.421 | 0.415 | 0.207  | 0.355 | 0.253 | 0.344  |
| BERT+Span    | 0.492 | 0.471 | 0.305  | 0.415 | 0.309 | 0.413  |

**Recall (R):**
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
