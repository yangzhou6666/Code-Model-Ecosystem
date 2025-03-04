'''analyze the results (accuracy, precision, recall) from OpenAI models'''

import os
import json
from build_batch_file import get_model_type

if __name__ == '__main__':
    
    path_to_labels = './data/manual-labeling.csv'
    model_to_type = get_model_type(path_to_labels)
    
    prompt_type = 'zero-shot-CoT'
    # prompt_type = 'zero-shot-prompt'
    openai_model_type = 'gpt-4o'
    # openai_model_type = 'gpt-3.5-turbo'
    
    output_file = './batches/{}-{}-output.jsonl'.format(prompt_type, openai_model_type)
    assert os.path.exists(output_file), f'{output_file} does not exist'

    correct_cnt = 0
    cnt_yes = sum(1 for v in model_to_type.values() if v == 'yes')
    cnt_no = sum(1 for v in model_to_type.values() if v == 'no')
    
    true_positive = 0
    false_positive = 0
    false_negative = 0
    
    with open(output_file) as f:
        lines = f.readlines()
        for line in lines:
            line = json.loads(line)
            model_name = line['custom_id']
            ground_truth = model_to_type[model_name]
            
            if openai_model_type == 'gpt-4o':
                llm_output = line['content'].lower()
            else:
                llm_output = line['response']["body"]['choices'][0]['message']['content'].lower()
            
            try:
                answer_region = llm_output.split('final answer')[1]
                if 'yes' in answer_region:
                    prediction = 'yes'
                elif 'no' in answer_region:
                    prediction = 'no'
                else:
                    prediction = 'unknown'
            except:
                prediction = 'unknown'
            
            if ground_truth == prediction:
                correct_cnt += 1
            if prediction == 'yes':
                if ground_truth == 'yes':
                    true_positive += 1
                else:
                    false_positive += 1
            if ground_truth == 'yes' and prediction != 'yes':
                false_negative += 1

    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    accuracy = correct_cnt / len(model_to_type) if model_to_type else 0

    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    
    # f1
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    print(f'F1: {f1:.4f}')