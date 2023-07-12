import torch
import argparse
import transformers

from dataset import SupervisedDataset, DataCollatorForSupervisedDataset

from utils import set_seed, print_trainable_parameters


from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from transformers import (AutoTokenizer, AutoModelForCausalLM,
                          BitsAndBytesConfig, Trainer,
                          TrainingArguments, DataCollatorForLanguageModeling)


def make_supervised_data_module(tokenizer: transformers.PreTrainedTokenizer, data_files):
    """Make dataset and collator for supervised fine-tuning."""
    train_dataset = SupervisedDataset(tokenizer=tokenizer, data_path=data_files['train'])
    valid_dataset = SupervisedDataset(tokenizer=tokenizer, data_path=data_files['valid'])
    data_collator = DataCollatorForSupervisedDataset(tokenizer=tokenizer)
    return dict(train_dataset=train_dataset, eval_dataset=valid_dataset,
                data_collator=data_collator)


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

    # LOAD TOKENIZER
    tokenizer = AutoTokenizer.from_pretrained(
        args.checkpoint,
        use_fast=False,
        truncation_side='left',
        )

    # LOAD DATASET FROM LOCAL FILES
    data_files = {
        'train': '../preprocess/train.csv',
        'valid': '../preprocess/valid.csv',
        'test': '../preprocess/test.csv'
    }
    
    data_module = make_supervised_data_module(tokenizer=tokenizer, data_files=data_files)

    # LOAD MODEL
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
    
    # LOAD TRAINER
    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=TrainingArguments(
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=4,
            logging_steps=args.logging_steps,
            learning_rate=args.lr,
            warmup_steps=2,
            output_dir='outputs',
            optim='paged_adamw_8bit',
            report_to='none',
            num_train_epochs=args.epoch
        ),
        **data_module
    )
    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    trainer.train()


def get_args():
    parser = argparse.ArgumentParser(description='Dialogue Generation for prompt')
    parser.add_argument('--checkpoint', help='the model name', default='beomi/kollama-13b',
                        choices=['beomi/kollama-7b', 'beomi/kollama-13b'])

    parser.add_argument('--seed', type=int, help='seed', default=42)
    parser.add_argument('--batch_size', type=int, help='batch_size', default=4)
    parser.add_argument('--epoch', type=int, help='training epochs', default=5)
    parser.add_argument("--lr", type=float, help="learning rate", default=1e-4)

    parser.add_argument('--max_steps', type=int, help='training steps', default=1000)
    parser.add_argument('--logging_steps', type=int, help='logging step', default=50)    

    args = parser.parse_args()
    
    return args


if __name__ == '__main__':
    main()