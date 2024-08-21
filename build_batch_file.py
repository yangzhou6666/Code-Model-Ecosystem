import os 
import csv
import json
from pydantic import BaseModel


def get_query(prompt_type: str, model_name: str, readme: str, openai_model_type: str):

    if prompt_type == 'zero-shot-prompt':
        prompt = '''
            Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please provide your answer in either Yes or No Don't provide any other information. Your answer should be in the following template.

            Final Answers: Yes or No

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
        Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please explain the reason process of reaching the answer. You may want to analyze the model's training data, tasks, and evaluation dataset. You must provide your final answer in either Yes or No. You cannot say unsure. Your answer should be in the following template.

        Reason Steps:

        Final Answers: Yes or No
        
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
        pass
        # 这里query的结构要有所变化
        
        # example 1
        # message from the user
        prompt1 = "\n        Given the documentation (written in Markdown) of a Hugging Face model, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please explain the reason process of reaching the answer. You may want to analyze the model's training data, tasks, and evaluation dataset. You must provide your final answer in either Yes or No. You cannot say unsure. Your answer should be in the following template.\n\n        Reason Steps:\n\n        Final Answers: Yes or No\n        \n        ``` \n---\nlicense: apache-2.0\ntags:\n- text-classification\n---\n\n# Clinical BERT for ICD-10 Prediction\n\nThe Publicly Available Clinical BERT Embeddings paper contains four unique clinicalBERT models: initialized with BERT-Base (cased_L-12_H-768_A-12) or BioBERT (BioBERT-Base v1.0 + PubMed 200K + PMC 270K) & trained on either all MIMIC notes or only discharge summaries.  \n \n---\n\n## How to use the model\n\nLoad the model via the transformers library:\n\n    from transformers import AutoTokenizer, BertForSequenceClassification\n    tokenizer = AutoTokenizer.from_pretrained(\"AkshatSurolia/ICD-10-Code-Prediction\")\n    model = BertForSequenceClassification.from_pretrained(\"AkshatSurolia/ICD-10-Code-Prediction\")\n    config = model.config\n\nRun the model with clinical diagonosis text:\n\n    text = \"subarachnoid hemorrhage scalp laceration service: surgery major surgical or invasive\"\n    encoded_input = tokenizer(text, return_tensors='pt')\n    output = model(**encoded_input)\n\nReturn the Top-5 predicted ICD-10 codes:\n\n    results = output.logits.detach().cpu().numpy()[0].argsort()[::-1][:5]\n    return [ config.id2label[ids] for ids in results]```"
        
        # answer 1 from the assitant
        answer1 = "\nReason Steps:\n\n1. The model is called \"Clinical BERT for ICD-10 Prediction,\" indicating its focus on predicting ICD-10 diagnosis codes in the clinical domain.\n2. The model is trained on clinical notes and discharge summaries from the MIMIC dataset, which is related to healthcare and medical text rather than software engineering.\n3. The model uses clinical diagnosis text as input for prediction, further emphasizing its healthcare-related tasks.\n4. The model's primary function is to predict ICD-10 codes based on clinical text, which is a task within the medical domain and not software engineering.\n  \nFinal Answer: No"
        
        prompt2 = "\n        Given the documentation (written in Markdown) of a Hugging Face model SEBIS/code_trans_t5_base_api_generation, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please explain the reason process of reaching the answer. You may want to analyze the model's training data, tasks, and evaluation dataset. You must provide your final answer in either Yes or No. You cannot say unsure. Your answer should be in the following template.\n\n        Reason Steps:\n\n        Final Answers: Yes or No\n        \n        ``` \n---\ntags:\n- summarization\nwidget:\n- text: \"parse the uses licence node of this package , if any , and returns the license definition if theres\"\n\n---\n\n\n# CodeTrans model for api recommendation generation\nPretrained model for api recommendation generation using the t5 base model architecture. It was first released in\n[this repository](https://github.com/agemagician/CodeTrans). \n\n\n## Model description\n\nThis CodeTrans model is based on the `t5-base` model. It has its own SentencePiece vocabulary model. It used single-task training on Api Recommendation Generation dataset.\n\n## Intended uses & limitations\n\nThe model could be used to generate api usage for the java programming tasks. \n\n### How to use\n\nHere is how to use this model to generate java function documentation using Transformers SummarizationPipeline:\n\n```python\nfrom transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline\n\npipeline = SummarizationPipeline(\n    model=AutoModelWithLMHead.from_pretrained(\"SEBIS/code_trans_t5_base_api_generation\"),\n    tokenizer=AutoTokenizer.from_pretrained(\"SEBIS/code_trans_t5_base_api_generation\", skip_special_tokens=True),\n    device=0\n)\n\ntokenized_code = \"parse the uses licence node of this package , if any , and returns the license definition if theres\"\npipeline([tokenized_code])\n```\nRun this example in [colab notebook](https://github.com/agemagician/CodeTrans/blob/main/prediction/single%20task/api%20generation/base_model.ipynb).\n## Training data\n\nThe supervised training tasks datasets can be downloaded on [Link](https://www.dropbox.com/sh/488bq2of10r4wvw/AACs5CGIQuwtsD7j_Ls_JAORa/finetuning_dataset?dl=0&subfolder_nav_tracking=1)\n\n\n## Evaluation results\n\nFor the code documentation tasks, different models achieves the following results on different programming languages (in BLEU score):\n\nTest results :\n\n|   Language / Model   |      Java      |\n| -------------------- | :------------: |\n|   CodeTrans-ST-Small    |     68.71      |\n|   CodeTrans-ST-Base     |     70.45      |\n|   CodeTrans-TF-Small    |     68.90      |\n|   CodeTrans-TF-Base     |     72.11      |\n|   CodeTrans-TF-Large    |     73.26      |\n|   CodeTrans-MT-Small    |     58.43      |\n|   CodeTrans-MT-Base     |     67.97      |\n|   CodeTrans-MT-Large    |     72.29      |\n|   CodeTrans-MT-TF-Small |     69.29      |\n|   CodeTrans-MT-TF-Base  |     72.89      |\n|   CodeTrans-MT-TF-Large |   **73.39**    |\n|   State of the art   |     54.42      |\n\n\n\n> Created by [Ahmed Elnaggar](https://twitter.com/Elnaggar_AI) | [LinkedIn](https://www.linkedin.com/in/prof-ahmed-elnaggar/) and Wei Ding | [LinkedIn](https://www.linkedin.com/in/wei-ding-92561270/)\n\n```"
        
        answer2 = "Reason Steps:\n1. The model is named **SEBIS/code_trans_t5_base_api_generation** which implies it is focused on API generation.\n2. The model description specifies that it is used for generating API usage for Java programming tasks.\n3. The training data used for this model is the Api Recommendation Generation dataset.\n4. The evaluation results show that the model is specifically evaluated for code documentation tasks on different programming languages, including Java.\n5. The model achieves competitive BLEU scores compared to other CodeTrans models and surpasses the state of the art in code documentation.\n\nFinal Answer: Yes"
        
        prompt = '''
        Given the documentation (written in Markdown) of a Hugging Face model {}, please help me decide whether this model is designed for software engineering related tasks (like code completion, code generation, defect prediction, clone detection, and others). Please explain the reason process of reaching the answer. You may want to analyze the model's training data, tasks, and evaluation dataset. You must provide your final answer in either Yes or No. You cannot say unsure. Your answer should be in the following template.

        Reason Steps:

        Final Answers: Yes or No
        
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
        raise ValueError(f"Unknown prompt type: {prompt_type}")

    return qeury_json

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
    openai_model_type = 'gpt-4o'

    model_to_type = get_model_type(path_to_labels)
    
    
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
        
            qeury_json = get_query(prompt_type, model_name, readme, openai_model_type)
        
        # write the query to the file
        with open('./batches/{}-{}.jsonl'.format(prompt_type, openai_model_type), 'a') as f:
            json.dump(qeury_json, f)
            f.write('\n')

        

    