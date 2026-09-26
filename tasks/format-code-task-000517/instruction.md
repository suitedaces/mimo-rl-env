I get ValueError when trying to run Axoltlt on pretraining dataset
I am having the same issue except my dataset is not large (144 records). I want to finetune a model and my yaml is like this: 

```yaml
base_model: meta-llama/Meta-Llama-3-8B
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true
strict: false

max_steps: 100
pretraining_dataset:
   - path: dummy_dataset
     type: completion # (I also tried `pretrain`)
dataset_prepared_path:
val_set_size: 0.3
output_dir: ./outputs/finetuned_model

adapter: qlora
lora_model_dir:

sequence_len: 8192
sample_packing: false
eval_sample_packing: false
pad_to_sequence_len: false

lora_r: 16
lora_alpha: 16
lora_dropout: 0
lora_target_modules: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
lora_target_linear: true
lora_fan_in_fan_out:

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

gradient_accumulation_steps: 1
micro_batch_size: 8
num_epochs: 2
optimizer: paged_adamw_32bit
lr_scheduler: cosine
learning_rate: 0.0002

train_on_inputs: false
group_by_length: false
bf16: auto
fp16: true
tf32: false

gradient_checkpointing: true
early_stopping_patience:
resume_from_checkpoint:
local_rank:
logging_steps: 4
xformers_attention:
flash_attention: true

warmup_steps: 2
evals_per_epoch: 1
saves_per_epoch: 1
debug:
deepspeed:
weight_decay: 0.0
fsdp:
fsdp_config:
special_tokens:
```

And my dataset is in JSONL format following this format: 

```jsonl
{"text": ""}
{"text": ""}
...
```

And I keep getting: 

```
[rank0]: Traceback (most recent call last):
[rank0]:   File "<frozen runpy>", line 198, in _run_module_as_main
[rank0]:   File "<frozen runpy>", line 88, in _run_code
[rank0]:   File "/home/axolotl/src/axolotl/cli/train.py", line 70, in <module>
[rank0]:     fire.Fire(do_cli)
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/fire/core.py", line 143, in Fire
[rank0]:     component_trace = _Fire(component, args, parsed_flag_args, context, name)
[rank0]:                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/fire/core.py", line 477, in _Fire
[rank0]:     component, remaining_args = _CallAndUpdateTrace(
[rank0]:                                 ^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/fire/core.py", line 693, in _CallAndUpdateTrace
[rank0]:     component = fn(*varargs, **kwargs)
[rank0]:                 ^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/axolotl/src/axolotl/cli/train.py", line 38, in do_cli
[rank0]:     return do_train(parsed_cfg, parsed_cli_args)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/axolotl/src/axolotl/cli/train.py", line 66, in do_train
[rank0]:     return train(cfg=cfg, cli_args=cli_args, dataset_meta=dataset_meta)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/axolotl/src/axolotl/train.py", line 170, in train
[rank0]:     trainer.train(resume_from_checkpoint=resume_from_checkpoint)
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/transformers/trainer.py", line 1539, in train
[rank0]:     return inner_training_loop(
[rank0]:            ^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/transformers/trainer.py", line 1836, in _inner_training_loop
[rank0]:     for step, inputs in enumerate(epoch_iterator):
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/accelerate/data_loader.py", line 677, in __iter__
[rank0]:     next_batch, next_batch_info = self._fetch_batches(main_iterator)
[rank0]:                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/accelerate/data_loader.py", line 631, in _fetch_batches
[rank0]:     batches.append(next(iterator))
[rank0]:                    ^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/torch/utils/data/dataloader.py", line 631, in __next__
[rank0]:     data = self._next_data()
[rank0]:            ^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/torch/utils/data/dataloader.py", line 675, in _next_data
[rank0]:     data = self._dataset_fetcher.fetch(index)  # may raise StopIteration
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/torch/utils/data/_utils/fetch.py", line 32, in fetch
[rank0]:     data.append(next(self.dataset_iter))
[rank0]:                 ^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/datasets/iterable_dataset.py", line 1389, in __iter__
[rank0]:     for key, example in ex_iterable:
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/datasets/iterable_dataset.py", line 679, in __iter__
[rank0]:     yield from self._iter()
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/datasets/iterable_dataset.py", line 718, in _iter
[rank0]:     transformed_batch.update(self.function(*function_args, **self.fn_kwargs))
[rank0]:                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/axolotl/src/axolotl/utils/data/pretraining.py", line 23, in encode_pretraining
[rank0]:     res = tokenizer(
[rank0]:           ^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/transformers/tokenization_utils_base.py", line 2803, in __call__
[rank0]:     encodings = self._call_one(text=text, text_pair=text_pair, **all_kwargs)
[rank0]:                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/home/bsci/venv/lib/python3.11/site-packages/transformers/tokenization_utils_base.py", line 2862, in _call_one
[rank0]:     raise ValueError(
[rank0]: ValueError: text input must be of type `str` (single example), `List[str]` (batch or single pretokenized example) or `List[List[str]]` (batch of pretokenized examples).
```

_Originally posted by @Ahmedn1 in https://github.com/OpenAccess-AI-Collective/axolotl/issues/1597#issuecomment-2183299595_
