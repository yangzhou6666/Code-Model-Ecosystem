'''analyze the results (accuracy) from OpenAI models'''


import os
import json
from build_batch_file import get_model_type

if __name__ == '__main__':
    
    path_to_labels = './data/manual-labeling.csv'
    model_to_type = get_model_type(path_to_labels)
    
    prompt_type = 'zero-shot-prompt'
    openai_model_type = 'gpt-4o-mini'
    
    # get output file
    output_file = './batches/{}-{}-output.jsonl'.format(prompt_type, openai_model_type)
    assert os.path.exists(output_file), f'{output_file} does not exist'

    
    correct_cnt = 0
    
    # read the output file
    with open(output_file) as f:
        lines = f.readlines()
        for line in lines:
            line = json.loads(line)
            model_name = line['custom_id']
            ground_truth = model_to_type[model_name]
            
            # process the output
            llm_output = line['response']["body"]['choices'][0]['message']['content'].lower()
            try:
                answer_region = llm_output.split('final answer')[1]
            except:
                prediction = 'unknown'
                
            print(answer_region)
                
            
            # get prediction
            if 'yes' in answer_region:
                prediction = 'yes'
            elif 'no' in answer_region:
                prediction = 'no'
            else:
                prediction = 'unknown'
            
            if ground_truth == prediction:
                correct_cnt += 1
    
    print(f'Accuracy: {correct_cnt * 1.0 /len(model_to_type)}')
    # compute precision
            
            

    
    
    
    
    