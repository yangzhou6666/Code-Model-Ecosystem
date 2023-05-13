'''Analyze the models and datasets on HF'''

import os
import json

def analyze_license(model_dict):
    total_model = len(model_dict)
    num_model_with_license = 0

    license_dict = {}
    for model_name in model_dict:
        model_info = model_dict[model_name]
        license = None
        try:
            tags = model_info['tags']
        except:
            print(f'No tags for {model_name}')
            continue
        contain_license = False
        for tag in tags:
            if 'license' in tag:
                contain_license = True
                license = tag

        if contain_license is False:
            pass
        else:
            num_model_with_license += 1
            if license in license_dict:
                license_dict[license] += 1
            else:
                license_dict[license] = 1

    
    print(f'Total model: {total_model}')
    print(f'Number of models with license: {num_model_with_license}')
    print(f'Number of unique licenses: {len(license_dict)}')
    print(f'Unique licenses: {license_dict}')


if __name__ == '__main__':
    # read the detailed model info
    save_dir = 'data'
    with open(f'{save_dir}/model_detail_dict.json', 'r') as f:
        model_detail_dict = json.load(f)

    analyze_license(model_detail_dict)

    
    