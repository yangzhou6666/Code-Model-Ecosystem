import os 
import csv
import json
from build_batch_file_model_type import get_model_type

def get_query(prompt_type: str, model_name: str, readme: str, openai_model_type: str):
    if prompt_type == 'zero-shot-prompt':
        prompt = '''
            Given the documentation (written in Markdown) of a Hugging Face model, please help me decide whether this model is derived from another model (also called the parent model). The model can be derived by "sharing the architecture, fine-tuning a model, quantized from a model, model conversion" Please provide the parent model name extracted from the documentation. If there is no information about the base model, please put "unknow". Don't provide any other information. Your answer should be in the following template.
            
            parent model: model name

            '''.format(model_name)
            
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
        Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide whether this model is derived from another model (also called the parent model). The model can be derived by "sharing the architecture, fine-tuning a model, quantized from a model, model conversion" Please provide the parent model name extracted from the documentation. Provide how you reason to get the answer. If there is no information about the base model, please put "unknow". Don't provide any other information. Your answer should be in the following template.
        
            Reason Steps:
            
            parent model: model name
        
        '''.format(model_name)
        
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
        
    else: 
        raise ValueError('prompt_type is not supported')
    
    return qeury_json


if __name__ == '__main__':
    
    path_to_labels = './data/manual-labeling.csv'
    rdm_folder = 'readme-all'
    prompt_type = 'zero-shot-CoT'
    openai_model_type = 'gpt-4o-mini'

    model_to_type = get_model_type(path_to_labels)
    # only keep code models "value is yes"
    model_lists = [k for k, v in model_to_type.items() if v == 'yes']
    
    # remove the existing file ./batches/{prompt-type}-{model}.jsonl
    if os.path.exists('./batches/base-model/{}-{}.jsonl'.format(prompt_type, openai_model_type)):
        os.remove('./batches/base-model/{}-{}.jsonl'.format(prompt_type, openai_model_type))
    
    for model_name in model_lists:
        # get its documentation
        rdm = model_name.replace('/', '--') + '.md'
        
        with open(os.path.join(rdm_folder, rdm), 'r') as f:
            readme = f.read()
            
            qeury_json = get_query(prompt_type, model_name, readme, openai_model_type)
        
        # write the query to the file
        with open('./batches/base-model/{}-{}.jsonl'.format(prompt_type, openai_model_type), 'a') as f:
            json.dump(qeury_json, f)
            f.write('\n')
    