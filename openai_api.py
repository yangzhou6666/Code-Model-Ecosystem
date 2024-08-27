import os
from openai import OpenAI
import json
import time


if __name__ == '__main__':
    prompt_type = 'few-shot-CoT'
    openai_model_type = 'gpt-4o'
    # path to query
    task_type = "base-model"
    path_to_qeury = './batches/{}/{}-{}.jsonl'.format(task_type, prompt_type, openai_model_type)


    if os.path.exists('./batches/{}/{}-{}-output.jsonl'.format(task_type, prompt_type, openai_model_type)):
        os.remove('./batches/{}/{}-{}-output.jsonl'.format(task_type, prompt_type, openai_model_type))
        
    client = OpenAI()
    with open(path_to_qeury, 'r') as f:
        time.sleep(2)
        for line in f:
            data = json.loads(line)
            query = data['body']
            model = query['model']
            messages = query['messages']
            
    
            completion = client.chat.completions.create(
                model=model,
                messages=messages
            )
    
            output = completion.choices[0].message.content
            print(output)
            
            # store output into json
            result = {
                'custom_id': data['custom_id'],
                'content': output
            }
            
            with open('./batches/{}/{}-{}-output.jsonl'.format(task_type, prompt_type, openai_model_type), 'a') as f:
                f.write(json.dumps(result) + '\n')
            
            
    
    