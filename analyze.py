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

def model_data_dependency(model_dict):
    total_model = len(model_dict)
    num_model_with_data_info = 0

    data_dict = {}
    dependency_dict = {}
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
            if 'dataset' in tag:
                contain_license = True
                license = tag.split(':')[1]

        if contain_license is False:
            pass
        else:
            num_model_with_data_info += 1
            if license in data_dict:
                data_dict[license] += 1
            else:
                data_dict[license] = 1
            dependency_dict[model_name] = license

    print(f'Total model: {total_model}')
    print(f'Number of models with dataset info: {num_model_with_data_info}')
    print(f'Number of unique dataset: {len(data_dict)}')
    print(f'Unique dataset: {data_dict}')

    # save to csv file
    with open('data/model_data_dependency.csv', 'w') as f:
        for model_name in dependency_dict:
            f.write(f'{model_name},{dependency_dict[model_name]}\n')


if __name__ == '__main__':
    # read the detailed model info
    save_dir = 'data'
    with open(f'{save_dir}/model_detail_dict.json', 'r') as f:
        model_detail_dict = json.load(f)

    analyze_license(model_detail_dict)

    # read the dataset list
    with open(f'{save_dir}/dataset_dict.json', 'r') as f:
        dataset_list = json.load(f)
    
    model_data_dependency(model_detail_dict)

    
    