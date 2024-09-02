import os 
import csv
import json


def get_query(prompt_type: str, model_name: str, readme: str, openai_model_type: str, parent_model: str):
    '''produce prompts'''    
    if prompt_type == 'zero-shot-prompt':
        prompt = '''
            Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide how this model is reused and derived from its parent model {}. The reuse type include continue (a model uses the parameters of another model and continue to pre-train on other datasets.), finetune (a model fine-tunes another model on other datasets.), instruction-tuned (a model fine-tunes another on a collection of tasks described using instructions), adapter (a model is obtained by adding adapers (e.g., lora) to existing weights of a model), quantize (a model is quantized from another model), conversion (a model is converted from another model using a converter, e.g., ONNX), adversarial (a model is adversarially trained on another model to improve robustness), distillation (a model is obtained by knowledge distillation), and architecture (a model shares the architecture of another model but do not reuse its parameters). If there is no information about the reuse type, please put "unclear". Don't provide any other information. Your answer should be in the following template.
            
            dependency: reuse type

            '''.format(model_name, parent_model)
            
        question = prompt + '``` \n' + readme + '```'
    
        qeury_json = {
                "custom_id": model_name,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": openai_model_type,
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    "max_tokens": 1000
                }
        }
    elif prompt_type == 'zero-shot-CoT':
        prompt = '''
            Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide how this model is reused and derived from its parent model {}. The reuse type include continue (a model uses the parameters of another model and continue to pre-train on other datasets.), finetune (a model fine-tunes another model on other datasets.), instruction-tuned (a model fine-tunes another on a collection of tasks described using instructions), adapter (a model is obtained by adding adapers (e.g., lora) to existing weights of a model), quantize (a model is quantized from another model), conversion (a model is converted from another model using a converter, e.g., ONNX), adversarial (a model is adversarially trained on another model to improve robustness), distillation (a model is obtained by knowledge distillation), and architecture (a model shares the architecture of another model but do not reuse its parameters). If there is no information about the reuse type, please put "unclear". Please provide your reason steps to reach your answer. Your answer should be in the following template.
            
            reason steps: 
            
            dependency: reuse type

            '''.format(model_name, parent_model)
            
        question = prompt + '``` \n' + readme + '```'
    
        qeury_json = {
                "custom_id": model_name,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": openai_model_type,
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    "max_tokens": 1000
                }
        }
    elif prompt_type == 'few-shot-CoT':
        # example 1
        # message from the user
        prompt1 = '''\n                
        
        Given the documentation (written in Markdown) of a Hugging Face model SEBIS/code_trans_t5_base_api_generation_multitask_finetune, please help me decide how this model is reused and derived from its parent model. The reuse type include continue (a model uses the parameters of another model and continue to pre-train on other datasets.), finetune (a model fine-tunes another model on other datasets.), instruction-tuned (a model fine-tunes another on a collection of tasks described using instructions), adapter (a model is obtained by adding adapers (e.g., lora) to existing weights of a model), quantize (a model is quantized from another model), conversion (a model is converted from another model using a converter, e.g., ONNX), adversarial (a model is adversarially trained on another model to improve robustness), distillation (a model is obtained by knowledge distillation), and architecture (a model shares the architecture of another model but do not reuse its parameters). If there is no information about the reuse type, please put "unclear". Don't provide any other information. Your answer should be in the following template.
        
        reason steps: 
        
        dependency: reuse type
            
        ``` \n---\ntags:\n- summarization\nwidget:\n- text: \"parse the uses licence node of this package , if any , and returns the license definition if theres\"\n\n---\n\n\n# CodeTrans model for api recommendation generation\nPretrained model for api recommendation generation using the t5 base model architecture. It was first released in\n[this repository](https://github.com/agemagician/CodeTrans). \n\n\n## Model description\n\nThis CodeTrans model is based on the `t5-base` model. It has its own SentencePiece vocabulary model. It used multi-task training on 13 supervised tasks in the software development domain and 7 unsupervised datasets. It is then fine-tuned on the api recommendation generation task for the java apis.\n\n## Intended uses & limitations\n\nThe model could be used to generate api usage for the java programming tasks.```
        
        '''
        
        # answer 1 from the assitant
        answer1 = "\nreason steps:\n\n1. The documentation mentions that It is then fine-tuned on the api recommendation generation task for the java apis 2. fine-tune falls into the category finetune. \n dependency: finetune"
        
        prompt2 = '''\n                        Given the documentation (written in Markdown) of a Hugging Face model Xenova/codegen-350M-multi, please help me decide how this model is reused and derived from its parent model. The reuse type include continue (a model uses the parameters of another model and continue to pre-train on other datasets.), finetune (a model fine-tunes another model on other datasets.), instruction-tuned (a model fine-tunes another on a collection of tasks described using instructions), adapter (a model is obtained by adding adapers (e.g., lora) to existing weights of a model), quantize (a model is quantized from another model), conversion (a model is converted from another model using a converter, e.g., ONNX), adversarial (a model is adversarially trained on another model to improve robustness), distillation (a model is obtained by knowledge distillation), and architecture (a model shares the architecture of another model but do not reuse its parameters). If there is no information about the reuse type, please put "unclear". Don't provide any other information. Your answer should be in the following template.

        
        reason steps: 
        
        dependency: reuse type
            
        ``` ---\n
        library_name: "transformers.js"
        ---
        https://huggingface.co/Salesforce/codegen-350M-multi with ONNX weights to be compatible with Transformers.js.

        Note: Having a separate repo for ONNX weights is intended to be a temporary solution until WebML gains more traction. If you would like to make your models web-ready, we recommend converting to ONNX using [🤗 Optimum](https://huggingface.co/docs/optimum/index) and structuring your repo like this one (with ONNX weights located in a subfolder named `onnx`).```
        
        '''
        
        answer2 = "Reason Steps:\n1. The model mentions its the ONNX version of a model in url https://huggingface.co/Salesforce/codegen-350M-multi. 2. ONNX is another format of a model converted using ONNIX. 3. The reuse type falls into conversion type. \n\ndependency: conversion"
        
        prompt = '''
            Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide how this model is reused and derived from its parent model {}. The reuse type include continue (a model uses the parameters of another model and continue to pre-train on other datasets.), finetune (a model fine-tunes another model on other datasets.), instruction-tuned (a model fine-tunes another on a collection of tasks described using instructions), adapter (a model is obtained by adding adapers (e.g., lora) to existing weights of a model), quantize (a model is quantized from another model), conversion (a model is converted from another model using a converter, e.g., ONNX), adversarial (a model is adversarially trained on another model to improve robustness), distillation (a model is obtained by knowledge distillation), and architecture (a model shares the architecture of another model but do not reuse its parameters). If there is no information about the reuse type, please put "unclear". Please provide your reason steps to reach your answer. Your answer should be in the following template.
            
            reason steps: 
            
            dependency: reuse type

            '''.format(model_name, parent_model)
        
        question = prompt + '``` \n' + readme + '```'
        
        qeury_json = {
                "custom_id": model_name,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": openai_model_type,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt1
                        },
                        {
                            "role": "assistant",
                            "content": answer1,
                        },
                        {
                            "role": "user",
                            "content": prompt2
                        },
                        {
                            "role": "assistant",
                            "content": answer2,
                        },
                        {
                            "role": "user",
                            "content": question
                        },
                    ],
                    "max_tokens": 1000
                }
        }
    else:
        raise ValueError('prompt type not supported')

    return qeury_json

if __name__ == '__main__':
    # get the dependency type data
    path_to_labels = './data/model_dependency_new.csv'
    rdm_folder = 'readme-all'
    prompt_type = 'few-shot-CoT'
    openai_model_type = 'gpt-4o-mini'
    
    dependency_set = set(
        ['continue', 'finetune', 'unclear', 'instruction-tuned', 'adapter', 'quantize', 'conversion', 'adversarial', 'distillation', 'architecture']
    )
    
    model_to_dependency = {}
    model_to_base_model = {}
    with open(path_to_labels) as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            model_name = row[0]
            dependency_type = row[2].lower()
            # string is empty if the dependency type is not known
            if len(dependency_type) < 2:
                continue
            assert dependency_type in dependency_set, f'{dependency_type} is not in the dependency set'
            
            base_model = row[1].lower()
            
            model_to_dependency[model_name] = dependency_type
            model_to_base_model[model_name] = base_model
            
            

    # build batch file
    
    # remove if the file exists
    batch_file_path = './batches/dependency-type/{}-{}.jsonl'.format(prompt_type, openai_model_type)
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)
        
    for model_name in model_to_dependency.keys():
        # get its documentation
        rdm = model_name.replace('/', '--') + '.md'
        
        if not os.path.exists(os.path.join(rdm_folder, rdm)):
            print(f'{rdm} does not exist')
            
            link = f"https://huggingface.co/{model_name}/resolve/main/README.md"
            file_name = model_name.replace('/', '--')
            os.system(f"wget -O readme-all/{file_name}.md {link}")
            print(f"Downloaded {file_name}.md")
            
            
        # if the file size is smaller than 100 bytes, then it is not a valid file
        if os.path.getsize(os.path.join(rdm_folder, rdm)) < 100:
            print(f'{rdm} is not a valid file')
            continue
            
        with open(os.path.join(rdm_folder, rdm), 'r') as f:
            readme = f.read()
            
            qeury_json = get_query(prompt_type, model_name, readme, openai_model_type, model_to_base_model[model_name])
        
        # write the query to the file
        with open(batch_file_path, 'a') as f:
            f.write(json.dumps(qeury_json) + '\n')
        
        
    