import os
import json
import csv

def get_base_model(path_to_labels):
    model_to_base = {}

    # get the model and its type
    with open(path_to_labels) as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            model_name = row[0]
            
            if row[3] == '2':
                # means its a code model
                model_to_base[model_name] = row[1]
            
    return model_to_base

if __name__ == '__main__':
    path_to_labels = './data/model_dependency.csv'
    rdm_folder = 'readme-all'
    prompt_type = 'zero-shot-CoT'
    openai_model_type = 'gpt-4o-mini'

    model_to_base = get_base_model(path_to_labels)

    
    output_file = './batches/base-model/{}-{}-output.jsonl'.format(prompt_type, openai_model_type)
    assert os.path.exists(output_file), f'{output_file} does not exist'
    
    results = {}
    with open(output_file) as f:
        lines = f.readlines()
        for line in lines:
            line = json.loads(line)
            model_name = line['custom_id']
            try:
                ground_truth = model_to_base[model_name]
            except:
                print(model_name)
                continue
                
            
            if openai_model_type == 'gpt-4do':
                llm_output = line['content'].lower()
            else:
                llm_output = line['response']["body"]['choices'][0]['message']['content'].lower()
            
            llm_output = llm_output.split('parent model:')[1].strip()
            print(llm_output)
            results[model_name] = llm_output
            
            
            
    
    # save results to a csv file
    with open('./batches/base-model/{}-{}-output.csv'.format(prompt_type, openai_model_type), 'w') as f:
        f.write('model_name,ground_truth,prediction\n')
        for k, v in results.items():
            f.write(f'{k},{model_to_base[k]}, {v}\n')