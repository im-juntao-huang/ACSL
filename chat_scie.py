
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from tqdm import tqdm
import itertools
import json
import time
import openai

# Settings
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
api_key_list = ["sk-xxxxxxxxxxxxxxxxxxx", 
                "sk-xxxxxxxxxxxxxxxxxxx"] # 请填写你的 API KEY
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

def get_prompt(text):
    # prompt 设计
    prompt = \
    """
    你是一个科技文献领域的命名实体识别模型。现在我会给你一个句子，\
    请根据我的要求识别出所有句子中的实体，并用以JSON格式输出。\
    输出格式为JSON, 形如：{"entities": ["type": "类型1", "entity": "实体名"]}。\
    除了JSON以外请不要输出别的话。
    实体的定义如下:
    1.研究问题: 指的是要解决的问题、要构建的系统或要研发的应用程序等。   
    2.研究方法: 指的是所使用的方法、模型、框架、工具或系统等。
    3.评估度量: 指的是准确率、精度、性能等评价指标。
    4.研究材料: 指的是所使用的实验对象、数据集、实验平台或实验材料等。
    5.研究成果: 指的是所解决的问题、所验证的想法或者所提出的模型等。
    实体识别说明：
    1.尽可能识别实体的修饰词或限定词以使得实体的语义更加明确；
    2.在发生歧义时，总是倾向于较长的实体跨度；
    3.实体识别时不要改动原字段结构。
    给定句子：```<TEXT>```
    请识别：
    """
    
    return prompt.replace("<TEXT>", text)


# 设置 worker 函数
def worker(worker_id, text_id, raw_data):
    try:
        openai.api_key = api_key_list[text_id % len(api_key_list)]
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": get_prompt(raw_data[text_id])}
            ],
            timeout=60, # 设置超时时间为 60 秒
            temperature=0, # What sampling temperature to use, between 0 and 2. 
            # Higher values like 0.8 will make the output more random, 
            # while lower values like 0.2 will make it more focused and deterministic.
        )
    except Exception as e:
        # 异常发生时执行这里的代码
        # 出现网络错误时, 记录错误的 id
        print("==> 出现网络错误 at %d" % worker_id)
        print(f"==> 捕获到异常: {e}")
        error_idxs.append(text_id)
        return ""
    
    time.sleep(61) 
    # convert to json
    json_result = result['choices'][0]['message']['content']
    
    global total_nums_of_tokens
    total_nums_of_tokens += result['usage']['total_tokens']
    
    try:
        json_result = json.loads(json_result \
                                    .replace('```', '') \
                                    .replace('json', '') \
                                    .replace('\n', '') \
                                    .replace(' ', '') \
                                    .replace('，', ',') \
                                    .replace('。', ''))
        json_result['text'] = raw_data[text_id]
        json_result['text_id'] = text_id # 从 1 开始
    except: 
        # 非 json 格式错误
        error_idxs.append(text_id)
        print(json_result)
        print("==> 格式错误 at %d \n" % text_id)
        return ""
    
    return json_result


def main():
    # 读取数据
    file_path = "dataset/raw_data/csl_camera_readly_filter_cleaned.tsv"
    raw_data = read_data(file_path)
    
    # 设置处理区间 [start_idx, end_idx)
    start_idx, end_idx = 8049, 8050
    
    # 创建线程池
    num_workers = len(api_key_list) * 3 - 1  # 根据 api_key 的数量设置 worker 的数量
    executor = ThreadPoolExecutor(max_workers=num_workers)
    timeout = 60  # 设置超时时间，以秒为单位

    # 提交任务
    thread_id_list = list(range(num_workers)) 
    text_id_list =  list(range(start_idx, end_idx))
    combined_list = list(zip(itertools.cycle(thread_id_list), text_id_list))
    tasks = [executor.submit(worker, worker_id, text_id, raw_data) for worker_id, text_id in combined_list]

    # Create progress bar for tasks
    with tqdm(total=len(tasks)) as progress:

        # 等待所有任务完成或超时
        for future in as_completed(tasks):
            try:
                # 获取任务结果，处理超时异常
                result = future.result(timeout=timeout)
                progress.update(1)
            except TimeoutError:
                # 记录超时 id
                pending_task_id = tasks.index(future)
                print('thread %d timeout!' % pending_task_id)
                future.cancel()
                error_idxs.append(pending_task_id)

    # Get results for completed tasks
    results = [task.result() for task in tasks if task.done() and not task.cancelled() and task.result() != ""]

    print(f"==> {len(results)} threads completed.")

    if len(error_idxs) != 0:

        print("==> 存在异常 text_id：", error_idxs)
        print("==> 处理异常 ...")
        retry_time = 0
        while (len(error_idxs) != 0):
            # 处理错误的
            thread_id_list = list(range(num_workers)) 
            combined_list = list(zip(itertools.cycle(thread_id_list), error_idxs))
            new_tasks = [executor.submit(worker, i, j) for i, j in combined_list]
            error_idxs = []

            # Create progress bar for tasks
            with tqdm(total=len(new_tasks)) as progress:

                # 等待所有任务完成或超时
                for future in as_completed(new_tasks):
                    try:
                        # 获取任务结果，处理超时异常
                        result = future.result(timeout=timeout)
                        progress.update(1)
                    except TimeoutError:
                        # 记录超时 id
                        pending_task_id = tasks.index(future)
                        print('thread %d timeout!' % pending_task_id)
                        future.cancel()
                        error_idxs.append(pending_task_id)

            # Get results for completed tasks
            results += [task.result() for task in new_tasks if task.done() and not task.cancelled() and task.result() != ""]

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
    print(missing_values_list)
    error_idxs += missing_values_list

    print("==> 已完成数量：", len(results))
    print("==> 未完成数量：", len(error_idxs))

    print("==> 保存结果至：", 'output/annotation_{}_{}.json'.format(start_idx + 1, end_idx))
    save_file = 'output/annotation_{}_{}.json'.format(start_idx + 1, end_idx)
    with open(save_file, 'w', encoding='utf8') as f:
        json.dump(results, f, ensure_ascii=False)


    print("==> 保存错误id至： ", 'output/error_idxs.txt')
    with open('output/error_idxs.txt', 'a', encoding='utf8') as f:
        f.write(str(error_idxs))
        f.write('\n')

    print("==> 本次共消耗 token 数:", total_nums_of_tokens, "费用: $", total_nums_of_tokens * 0.002 / 4 / 1000, )
    print("==> 花费情况已保存至: output/api_cost.txt")
    with open('output/api_cost.txt', 'a', encoding='utf8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " ")
        f.write(str(total_nums_of_tokens * 0.002 / 4 / 1000))
        f.write('\n')