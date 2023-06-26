import os
import torch
import argparse

from utils import set_seed, print_trainable_parameters

from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForCausalLM,
                          BitsAndBytesConfig, Trainer,
                          TrainingArguments, DataCollatorForLanguageModeling)
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model


def main():
    # GET ARGS
    args = get_args()
    
    # SET SEED
    set_seed(seed=args.seed)

    # BitsAndBytes Config for QLoRA
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    # LOAD TOKENIZER & MODEL
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint)
    tokenizer.truncation_side='left'
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.checkpoint,
                                                 quantization_config=bnb_config,
                                                 device_map='auto')

    
    # PREPARE MODEL FOR K BIT TRAINING
    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    
    # LoRA Config
    config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=['q_proj', 'v_proj'], # model by model
        lora_dropout=0.05,
        bias='none',
        task_type='CAUSAL_LM'
    )

    # PREPARE MODEL FOR PEFT
    model = get_peft_model(model, config)
    print_trainable_parameters(model)
    
    # LOAD DATASET FROM LOCAL FILES
    data_files = {'train': 'train.csv', 'validation': 'valid.csv', 'test': 'test.csv'}
    dataset = load_dataset('../preprocess', data_files)

    def tokenization(example):
        return tokenizer(example['scenario'], truncation=True, padding=True, max_length=1024)    

    dataset = dataset.map(tokenization, batched=True, remove_columns=['prompt', 'input', 'output', 'scenario'])

    # LOAD TRAINER
    trainer = Trainer(
        model=model,
        train_dataset=dataset['train'],
        eval_dataset=dataset['validation'],
        args=TrainingArguments(
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=4,
            # max_steps=args.max_steps,
            logging_steps=args.logging_steps,
            learning_rate=args.lr,
            warmup_steps=2,
            # fp16=True,
            output_dir='outputs',
            optim='paged_adamw_8bit',
            report_to='none',
            num_train_epochs=args.epoch
        ),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    trainer.train()


def get_args():
    parser = argparse.ArgumentParser(description='Dialogue Generation for prompt')
    parser.add_argument('--checkpoint', help='the model name', default='beomi/kollama-7b',
                        choices=['beomi/kollama-7b', ''])

    parser.add_argument('--seed', type=int, help='seed', default=42)
    parser.add_argument('--batch_size', type=int, help='batch_size', default=4)
    parser.add_argument('--epoch', type=int, help='training epochs', default=5)
    parser.add_argument("--lr", type=float, help="learning rate", default=1e-4)

    parser.add_argument('--max_steps', type=int, help='training steps', default=1000)
    parser.add_argument('--logging_steps', type=int, help='logging step', default=50)
    
    # parser.add_argument('-dya', '--dyadic', action='store_true', help='dyadic conversation')    

    args = parser.parse_args()
    
    return args


if __name__ == '__main__':
    main()