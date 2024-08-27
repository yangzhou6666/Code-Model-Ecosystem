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
        
    elif prompt_type == 'few-shot-CoT':
        # example 1
        # message from the user
        prompt1 = '''\n                Given the documentation (written in Markdown) of a Hugging Face model SEBIS/code_trans_t5_base_api_generation_multitask_finetune, please help me decide whether this model is derived from another model (also called the parent model). The model can be derived by "sharing the architecture, fine-tuning a model, quantized from a model, model conversion" Please provide the parent model name extracted from the documentation. Provide how you reason to get the answer. If there is no information about the base model, please put "unknow". Don't provide any other information. Your answer should be in the following template.
        
            Reason Steps:
            
            parent model: model name
            
        ``` \n---\ntags:\n- summarization\nwidget:\n- text: \"parse the uses licence node of this package , if any , and returns the license definition if theres\"\n\n---\n\n\n# CodeTrans model for api recommendation generation\nPretrained model for api recommendation generation using the t5 base model architecture. It was first released in\n[this repository](https://github.com/agemagician/CodeTrans). \n\n\n## Model description\n\nThis CodeTrans model is based on the `t5-base` model. It has its own SentencePiece vocabulary model. It used multi-task training on 13 supervised tasks in the software development domain and 7 unsupervised datasets. It is then fine-tuned on the api recommendation generation task for the java apis.\n\n## Intended uses & limitations\n\nThe model could be used to generate api usage for the java programming tasks.```
        
        
        '''
        
        # answer 1 from the assitant
        answer1 = "\nReason Steps:\n\n1. The documentation mentions that the model is **fined tuned** on a another based on t5-base. 2. The closest parent is this another model. 3. based on the model name and the fine-tuning activity, the closed parent model is SEBIS/code_trans_t5_base_api_generation_multitask. \n parent model: SEBIS/code_trans_t5_base_api_generation_multitask"
        
        prompt2 = '''\n                Given the documentation (written in Markdown) of a Hugging Face model Xenova/codegen-350M-multi, please help me decide whether this model is derived from another model (also called the parent model). The model can be derived by "sharing the architecture, fine-tuning a model, quantized from a model, model conversion" Please provide the parent model name extracted from the documentation. Provide how you reason to get the answer. If there is no information about the base model, please put "unknow". Don't provide any other information. Your answer should be in the following template.
        
            Reason Steps:
            
            parent model: model name
            
        ``` ---\n
        library_name: "transformers.js"
        ---
        https://huggingface.co/Salesforce/codegen-350M-multi with ONNX weights to be compatible with Transformers.js.

        Note: Having a separate repo for ONNX weights is intended to be a temporary solution until WebML gains more traction. If you would like to make your models web-ready, we recommend converting to ONNX using [🤗 Optimum](https://huggingface.co/docs/optimum/index) and structuring your repo like this one (with ONNX weights located in a subfolder named `onnx`).```
        
        '''
        
        answer2 = "Reason Steps:\n1. The model mentions its the ONNX version of a model in url https://huggingface.co/Salesforce/codegen-350M-multi. 2. This url refers to Salesforce/codegen-350M-multi \n\nparent model: Salesforce/codegen-350M-multi"
        
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
        raise ValueError('prompt_type is not supported')
    
    return qeury_json


if __name__ == '__main__':
    
    path_to_labels = './data/manual-labeling.csv'
    rdm_folder = 'readme-all'
    prompt_type = 'few-shot-CoT'
    openai_model_type = 'gpt-4o'

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
    