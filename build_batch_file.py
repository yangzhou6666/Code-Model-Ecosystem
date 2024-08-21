import os 
import csv
import json
from pydantic import BaseModel


def get_prompt(prompt_type: str):
    if prompt_type == 'zero-shot-prompt':
        prompt = '''
            Given the documentation (written in Markdown) of a Hugging Face model, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please provide your answer in either Yes or No Don't provide any other information. Your answer should be in the following template.

            Final Answers: Yes or No

            '''
    elif prompt_type == 'zero-shot-CoT':
        prompt = '''
        Given the documentation (written in Markdown) of a Hugging Face model, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please explain the reason process of reaching the answer. You may want to analyze the model's training data, tasks, and evaluation dataset. You must provide your final answer in either Yes or No. You cannot say unsure. Your answer should be in the following template.

        Reason Steps:

        Final Answers: Yes or No
        
        '''
    elif prompt_type == 'few-shot-CoT':
        raise NotImplementedError
        # 这里需要设计一个few-shot的模板
    
    
    else:
        raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    return prompt

def get_model_type(path_to_labels):
    model_to_type = {}

    # get the model and its type
    with open(path_to_labels) as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            model_name = row[0]
            
            if row[2] == '2':
                model_type = 'yes'
            elif row[2] == '1':
                model_type = 'no'
            else:
                model_type = 'unknown'
                continue

            model_to_type[model_name] = model_type
            
    return model_to_type

if __name__ == '__main__':
    
    path_to_labels = './data/manual-labeling.csv'
    rdm_folder = 'readme-all'
    prompt_type = 'zero-shot-CoT'
    openai_model_type = 'gpt-3.5-turbo'

    model_to_type = get_model_type(path_to_labels)
    
    prompt = get_prompt(prompt_type)
    
    # remove the existing file ./batches/{prompt-type}-{model}.jsonl
    if os.path.exists('./batches/{}-{}.jsonl'.format(prompt_type, openai_model_type)):
        os.remove('./batches/{}-{}.jsonl'.format(prompt_type, openai_model_type))
    
    
    for model_name in model_to_type.keys():
        # get its documentation
        rdm = model_name.replace('/', '--') + '.md'
        if not os.path.exists(os.path.join(rdm_folder, rdm)):
            print(f'{rdm} does not exist and try to download')
            
            link = f"https://huggingface.co/{model_name}/resolve/main/README.md"
            file_name = model_name.replace('/', '--')
            os.system(f"wget -O readme-all/{file_name}.md {link}")
            print(f"Downloaded {file_name}.md")
            
        with open(os.path.join(rdm_folder, rdm), 'r') as f:
            readme = f.read()
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
        
        # write the query to the file
        with open('./batches/{}-{}.jsonl'.format(prompt_type, openai_model_type), 'a') as f:
            json.dump(qeury_json, f)
            f.write('\n')

        

    