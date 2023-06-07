CURRENT_DIR=`pwd`
export BERT_BASE_DIR=pretrained_models/hfl/chinese-roberta-wwm-ext
export DATA_DIR=$CURRENT_DIR/datasets
export OUTPUR_DIR=$CURRENT_DIR/outputs
TASK_NAME="acsl"

# export CUDA_VISIBLE_DEVICES="1,0"

python run_ner_span.py \
  --model_type=bert \
  --model_name_or_path=$BERT_BASE_DIR \
  --task_name=$TASK_NAME \
  --do_train \
  --do_predict \
  --do_adv \
  --eval_all_checkpoints \
  --do_lower_case \
  --loss_type=ce \
  --data_dir=$DATA_DIR/${TASK_NAME}/ \
  --train_max_seq_length=256 \
  --eval_max_seq_length=512 \
  --per_gpu_train_batch_size=48 \
  --per_gpu_eval_batch_size=48 \
  --learning_rate=2e-4 \
  --num_train_epochs=20.0 \
  --logging_steps=50 \
  --save_steps=50 \
  --output_dir=$OUTPUR_DIR/${TASK_NAME}_output_span/ \
  --overwrite_output_dir \
  --seed=45

