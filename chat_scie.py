
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from tqdm import tqdm
import itertools
import json
import time
import openai
from config import *

openai.api_key = api_key_list[0] # 默认 api_key

# global variables
total_nums_of_tokens = 0 # 记录总花销
error_idxs = [] # 记录错误 text_id

# Read data
def read_data(file_path):
    print(f"==> 读取科学文献数据 {file_path}, 并格式化...")
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    raw_data = []
    for line in lines:
        title, abstract = line.split('\t')[:2] # 题目, 摘要
        raw_data.append(abstract)
    print("==> 读取完成!")
    
    return raw_data

def get_prompt(text, type="ner"):
    # prompt v1
    # prompt_ner = \
    # """
    # 你是一个科技文献领域的命名实体识别模型。现在我会给你一个句子，\
    # 请根据我的要求识别出所有句子中的实体，并用以JSON格式输出。\
    # 输出格式为JSON, 形如：{"entities": ["type": "类型1", "entity": "实体名"]}。\
    # 除了JSON以外请不要输出别的话。
    # 实体的定义如下:
    # 1.研究问题: 指的是要解决的问题、要构建的系统或要研发的应用程序等。   
    # 2.研究方法: 指的是所使用的方法、模型、框架、工具或系统等。
    # 3.评估度量: 指的是准确率、精度、性能等评价指标。
    # 4.研究材料: 指的是所使用的实验对象、数据集、实验平台或实验材料等。
    # 5.研究成果: 指的是所解决的问题、所验证的想法或者所提出的模型等。
    # 实体识别说明：
    # 1.尽可能识别实体的修饰词或限定词以使得实体的语义更加明确；
    # 2.在发生歧义时，总是倾向于较长的实体跨度；
    # 3.实体识别时不要改动原字段结构。
    # 给定句子：```<TEXT>```
    # 请识别：
    # """
    
    prompt_ner = \
    """
    你是一个科技文献领域的命名实体识别模型。现在我会给你一篇中文科技文献的摘要，\
    请根据我的要求识别出所包含的所有实体，并用以JSON格式输出。\
    输出格式为JSON, 形如：{"entities": ["type": "类型1", "entity": "实体名"]}。\
    除了JSON以外请不要输出别的话。
    实体类型定义:
    - 研究问题: 指的是要解决什么问题、要构建什么系统或是要研发什么应用程序等等，用于描述研究目的语句；   
    - 研究方法: 指的是使用什么方法、什么模型、什么框架、什么工具或什么系统等等，用于描述研究方法的语句；
    - 研究材料: 指的是实验用了什么数据、什么材料或什么样本等等，用于描述实验对象的语句；
    - 研究成果: 指的是解决了什么问题、或形成了什么结论等，用于描述研究价值的语句。
    约束条件：
    - 你必须仔细思考实体类型的定义；
    - 你首先需要先找出摘要中的研究问题，接着再找出研究方法和研究材料，最后再找出研究成果，一步一步仔细思考；
    - 你必须仔细思考实体的语义边界，尽可能标注完整的句子；
    - 你不可以改动原字段结构。
    给定句子：```<TEXT>```
    请识别：
    """
    
    prompt_qa = \
    '''
    你是一名科技文献领域专家，请仔细阅读下面给出的中文科技文献的摘要内容，并告诉我这篇论文的研究问题是什么。\
    以陈述句的方式回答，要求简洁。
    将回答格式化为JSON格式，形如：{"answer": """研究问题"""} \
    为了避免格式错误，JSON中的回答必须包含在"""中。
    给定摘要：```<TEXT>```
    请回答：
    '''
    
    prompt_hub = {
        "ner": prompt_ner,
        "qa": prompt_qa
    }
    
    prompt = prompt_hub[type]
    
    return prompt.replace("<TEXT>", text)

def llm_chat(prompt, temperature=0):
    result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature, # What sampling temperature to use, between 0 and 2. 
            # Higher values like 0.8 will make the output more random, 
            # while lower values like 0.2 will make it more focused and deterministic.
        )
    return result['choices'][0]['message']['content'],  result['usage']['total_tokens']

def generation_parser(llm_result):
    
    return json.loads(llm_result.replace('```', '') \
                                .replace('json', '') \
                                .replace('\n', '') )

# 设置 task 函数
def task(thread_id, text_id, raw_data, type='ner'):
    try:
        openai.api_key = api_key_list[text_id % len(api_key_list)]
        promt = get_prompt(raw_data[text_id], type=type)
        llm_result, nums_of_tokens = llm_chat(promt)
        global total_nums_of_tokens
        total_nums_of_tokens += nums_of_tokens
    except Exception as e:
        # 出现网络错误时, 记录错误的 id
        print("==> 出现网络错误，线程 id: {}, text_id: {}".format(thread_id, text_id))
        print(f"==> 捕获到异常: {e}")
        error_idxs.append(text_id)
        return ""
    
    # 由于 OpenAI API 速率限制，每分钟只能调用 3 次，
    # 这里采用了多线程，每个 api_key 分配三个线程
    # 因此设置 61s 的间隔时间，刚好可以达到最大的速率。
    time.sleep(61) 
    
    try:
        json_object = generation_parser(llm_result) # 解析 LLM 输出
        json_object['text'] = raw_data[text_id] # 原始文本
        json_object['text_id'] = text_id # 文本 id，从 1 开始
    except: 
        # json 格式错误
        error_idxs.append(text_id)
        print("==> LLM 输出格式错误: text_id = %d \n" % text_id)
        print(llm_result)
        return ""
    
    return json_object


def main():
    # 读取数据
    file_path = "dataset/raw_data/csl_camera_readly_filter_cleaned.tsv"
    raw_data = read_data(file_path)
    
    # 设置标注任务类型
    type = 'ner'
    
    # 设置处理区间 [start_idx, end_idx)
    start_idx, end_idx = 0, 100
    
    # 创建线程池
    speed_limit = 32 # 小于每分钟调用 OpenAI API 的次数限制
    num_workers = len(api_key_list) * speed_limit - 1  # 根据 api_key 的数量设置 task 的数量
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # 提交任务
        thread_id_list = list(range(num_workers)) 
        text_id_list =  list(range(start_idx, end_idx))
        thread_text_list = list(zip(itertools.cycle(thread_id_list), text_id_list))
        futures = [executor.submit(task, thread_id, text_id, raw_data, type) for thread_id, text_id in thread_text_list]
        
        global error_idxs
        # Create progress bar for futures
        with tqdm(total=len(futures)) as progress:
            # 等待所有任务完成或超时
            for future in as_completed(futures):
                # 获取任务结果
                future.result()
                progress.update(1)

        # Get results for completed futures
        results = [future.result() for future in futures if future.done() and future.result() != ""]
        print(f"==> {len(results)} 个线程已完成.")

        # 处理异常 retry
        if len(error_idxs) != 0:
            print("==> 存在异常 text_id：", error_idxs)
            print("==> 处理异常 ...")
            retry_time = 0
            while (len(error_idxs) != 0):
                # 处理错误的
                thread_id_list = list(range(num_workers)) 
                combined_list = list(zip(itertools.cycle(thread_id_list), error_idxs))
                futures = [executor.submit(task, thread_id, text_id, raw_data) for thread_id, text_id in combined_list]
                error_idxs = []

                # Create progress bar for futures
                with tqdm(total=len(futures)) as progress:
                    # 等待所有任务完成
                    for future in as_completed(futures):
                        # 获取任务结果
                        future.result()
                        progress.update(1)

                # Get results for completed futures
                results += [future.result() for future in futures if future.done() and not future.cancelled() and future.result() != ""]

                print(f"==> {len(results)} threads completed.")

                retry_time += 1
                if (retry_time == 1):
                    print(f"==> 仍有以下错误 id，需手动处理： {error_idxs}")
                    break
    
    # 检测所有未完成处理的 id
    result_set = set([results[i]['text_id'] for i in range(len(results))])
    full_set = set(range(start_idx, end_idx))
    missing_values = full_set - result_set
    missing_values_list = list(missing_values)
    error_idxs = missing_values_list

    print("==> 已完成数量：", len(results))
    print("==> 未完成数量：", len(error_idxs))
    if len(error_idxs) != 0:
        print("==> 未完成 text_id：", error_idxs)

    save_annotation_file = f'output/{type}_annotation_{start_idx + 1}_{end_idx}.json'
    print("==> 保存结果至：", save_annotation_file)
    with open(save_annotation_file, 'w', encoding='utf8') as f:
        json.dump(results, f, ensure_ascii=False)

    save_error_id_file = f'output/{type}_error_idxs.txt'
    print("==> 保存错误id至： ", save_error_id_file)
    with open(save_error_id_file, 'w', encoding='utf8') as f:
        f.write(str(error_idxs))
        f.write('\n')

    save_cost_file = f'output/{type}_api_cost.txt'
    print("==> 本次共消耗 token 数:", total_nums_of_tokens, "费用: ", total_nums_of_tokens * 0.002 / 4 / 1000, )
    print("==> 花费情况已保存至: ", save_cost_file)
    with open(save_cost_file, 'a', encoding='utf8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " ")
        f.write('$'+str(total_nums_of_tokens * 0.002 / 4 / 1000))
        f.write('\n')
        
if __name__ == "__main__":
    main()