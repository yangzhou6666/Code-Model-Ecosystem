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
    path_to_labels = './data/model_dependency_new.csv'
    rdm_folder = 'readme-all'
    prompt_type = 'zero-shot-CoT'
    openai_model_type = 'gpt-4o'

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
            

    
    output_file = './batches/dependency-type/{}-{}-output.jsonl'.format(prompt_type, openai_model_type)
    assert os.path.exists(output_file), f'{output_file} does not exist'
    
    results = {}
    with open(output_file) as f:
        lines = f.readlines()
        for line in lines:
            line = json.loads(line)
            model_name = line['custom_id']
            try:
                ground_truth = model_to_dependency[model_name]
            except:
                print(model_name)
                # results[model_name] = 'unknown'
                # model_to_base[model_name] = 'unknown'
                continue
                
            
            if openai_model_type == 'gpt-4o':
                llm_output = line['content'].lower()
            else:
                llm_output = line['response']["body"]['choices'][0]['message']['content'].lower()
                
            llm_output = llm_output.replace(',', '--')
            
            try:
                llm_output = llm_output.split('depend')[1].strip()
            except:
                # not following the format
                
                llm_output = llm_output.replace('\n', '-')
                results[model_name] = llm_output
                print(model_name)
                
                continue

            # remove \n
            llm_output = llm_output.replace('\n', '-')
            results[model_name] = llm_output[0:40]
            
    
    # save results to a csv file
    with open('./batches/dependency-type/{}-{}-output.csv'.format(prompt_type, openai_model_type), 'w') as f:
        f.write('model_name,ground_truth,prediction\n')
        for k, v in results.items():
            f.write(f'{k},{model_to_dependency[k]}, {v}\n')
            