import argparse

def get_argparse():
    """
    GitHub Copilot: 以下是对该代码中参数的详细说明：

     `--cache_dir`：预训练模型下载的缓存目录，默认为空字符串。

     `--train_max_seq_length`：训练集中输入序列的最大长度，超过该长度的序列将被截断，小于该长度的序列将被填充，默认为128。
     `--eval_max_seq_length`：验证集中输入序列的最大长度，超过该长度的序列将被截断，小于该长度的序列将被填充，默认为512。

     `--do_train`：是否进行训练，默认为False。
     `--do_eval`：是否进行验证，默认为False。
     `--do_predict`：是否进行预测，默认为False。
     `--evaluate_during_training`：是否在训练过程中进行验证，默认为False。

     `--do_lower_case`：是否使用小写模型，默认为False。

     `--do_adv`：是否进行对抗训练，默认为False。
     `--adv_epsilon`：对抗训练的epsilon值，默认为1.0。
     `--adv_name`：对抗训练的层名称，默认为word_embeddings。

     `--per_gpu_train_batch_size`：每个GPU/CPU上的训练批次大小，默认为8。
     `--per_gpu_eval_batch_size`：每个GPU/CPU上的验证批次大小，默认为8。

     `--gradient_accumulation_steps`：累积梯度的步数，默认为1。

     `--learning_rate`：Adam优化器的初始学习率，默认为5e-5。
     `--crf_learning_rate`：CRF和线性层的初始学习率，默认为5e-5。

     `--weight_decay`：权重衰减系数，默认为0.01。

     `--adam_epsilon`：Adam优化器的epsilon值，默认为1e-8。

     `--max_grad_norm`：梯度的最大范数，默认为1.0。

     `--num_train_epochs`：训练的总轮数，默认为3.0。
     `--max_steps`：训练的总步数，如果设置为正数，则覆盖num_train_epochs，默认为-1。

     `--warmup_proportion`：学习率线性预热的比例，默认为0.1。

     `--logging_steps`：每隔多少步记录一次日志，默认为50。
     `--save_steps`：每隔多少步保存一次模型，默认为50。

     `--eval_all_checkpoints`：是否对所有检查点进行验证，默认为False。
     `--predict_checkpoints`：预测检查点的数量，默认为0。

     `--no_cuda`：是否禁用CUDA，默认为False。

     `--overwrite_output_dir`：是否覆盖输出目录中的内容，默认为False。
     `--overwrite_cache`：是否覆盖缓存的训练和验证集，默认为False。

     `--seed`：随机数生成器的种子，默认为42。

     `--fp16`：是否使用16位（混合）精度（通过NVIDIA apex）而不是32位，默认为False。
     `--fp16_opt_level`：对于fp16，选择Apex AMP优化级别，可选值为['O0'，'O1'，'O2'和'O3']，默认为O1。

     `--local_rank`：分布式训练的本地rank，默认为-1。

     `--server_ip`：远程调试的服务器IP地址，默认为空字符串。
     `--server_port`：远程调试的服务器端口号，默认为空字符串。
    
    """
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument("--task_name", default=None, type=str, required=True,
                        help="The name of the task to train selected in the list: ['cner', 'ACSL']")
    parser.add_argument("--data_dir", default=None, type=str, required=True,
                        help="The input data dir. Should contain the training files for the CoNLL-2003 NER task.", )
    parser.add_argument("--model_type", default=None, type=str, required=True,
                        help="Model type selected in the list: ['bert']")
    parser.add_argument("--model_name_or_path", default=None, type=str, required=True,
                        help="Path to pre-trained model or shortcut name selected in the list: " )
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.", )

    # Other parameters
    parser.add_argument('--markup', default='bios', type=str,
                        choices=['bios', 'bio'])
    parser.add_argument('--loss_type', default='ce', type=str,
                        choices=['lsr', 'focal', 'ce'])
    parser.add_argument("--config_name", default="", type=str,
                        help="Pretrained config name or path if not the same as model_name")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Pretrained tokenizer name or path if not the same as model_name", )
    parser.add_argument("--cache_dir", default="", type=str,
                        help="Where do you want to store the pre-trained models downloaded from s3", )
    parser.add_argument("--train_max_seq_length", default=128, type=int,
                        help="The maximum total input sequence length after tokenization. Sequences longer "
                             "than this will be truncated, sequences shorter will be padded.", )
    parser.add_argument("--eval_max_seq_length", default=512, type=int,
                        help="The maximum total input sequence length after tokenization. Sequences longer "
                             "than this will be truncated, sequences shorter will be padded.", )
    parser.add_argument("--do_train", action="store_true",
                        help="Whether to run training.")
    parser.add_argument("--do_eval", action="store_true",
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--do_predict", action="store_true",
                        help="Whether to run predictions on the test set.")
    parser.add_argument("--evaluate_during_training", action="store_true",
                        help="Whether to run evaluation during training at each logging step.", )
    parser.add_argument("--do_lower_case", action="store_true",
                        help="Set this flag if you are using an uncased model.")
    
    # adversarial training
    parser.add_argument("--do_adv", action="store_true",
                        help="Whether to adversarial training.")
    parser.add_argument('--adv_epsilon', default=1.0, type=float,
                        help="Epsilon for adversarial.")
    parser.add_argument('--adv_name', default='word_embeddings', type=str,
                        help="name for adversarial layer.")

    parser.add_argument("--per_gpu_train_batch_size", default=8, type=int,
                        help="Batch size per GPU/CPU for training.")
    parser.add_argument("--per_gpu_eval_batch_size", default=8, type=int,
                        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.", )
    parser.add_argument("--learning_rate", default=5e-5, type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument("--crf_learning_rate", default=5e-5, type=float,
                        help="The initial learning rate for crf and linear layer.")
    parser.add_argument("--weight_decay", default=0.01, type=float,
                        help="Weight decay if we apply some.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float,
                        help="Max gradient norm.")
    parser.add_argument("--num_train_epochs", default=3.0, type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--max_steps", default=-1, type=int,
                        help="If > 0: set total number of training steps to perform. Override num_train_epochs.", )

    parser.add_argument("--warmup_proportion", default=0.1, type=float,
                        help="Proportion of training to perform linear learning rate warmup for,E.g., 0.1 = 10% of training.")
    parser.add_argument("--logging_steps", type=int, default=50,
                        help="Log every X updates steps.")
    parser.add_argument("--save_steps", type=int, default=50, help="Save checkpoint every X updates steps.")
    parser.add_argument("--eval_all_checkpoints", action="store_true",
                        help="Evaluate all checkpoints starting with the same prefix as model_name ending and ending with step number", )
    parser.add_argument("--predict_checkpoints",type=int, default=0,
                        help="predict checkpoints starting with the same prefix as model_name ending and ending with step number")
    parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")
    parser.add_argument("--overwrite_output_dir", action="store_true",
                        help="Overwrite the content of the output directory")
    parser.add_argument("--overwrite_cache", action="store_true",
                        help="Overwrite the cached training and evaluation sets")
    parser.add_argument("--seed", type=int, default=42, help="random seed for initialization")
    parser.add_argument("--fp16", action="store_true",
                        help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit", )
    parser.add_argument("--fp16_opt_level", type=str, default="O1",
                        help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                             "See details at https://nvidia.github.io/apex/amp.html", )
    parser.add_argument("--local_rank", type=int, default=-1, help="For distributed training: local_rank")
    parser.add_argument("--server_ip", type=str, default="", help="For distant debugging.")
    parser.add_argument("--server_port", type=str, default="", help="For distant debugging.")
    return parser