'''play with huggingface API to obtain some information'''

import requests
import json
import yaml
import time
import csv

class HuggingFaceAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://huggingface.co"
        self.interval = 0.5 # seconds

    def set_interval(self, interval):
        self.interval = interval

    def get_model_list_by_keywords(self, keyword=None):
        endpoint = f"/api/models?search={keyword}"
        query_params = {
            # "search": keyword if isinstance(keyword, str) else ""}
        }
        
        all_models = []
        next_url = self.base_url + endpoint
        while next_url:
            response = requests.get(next_url, params=query_params)
            response_dict = json.loads(response.content)
            all_models.extend(response_dict)  # Add current page data to the list
            
            # Check if there's a next page
            next_url = response.links.get('next', {}).get('url', None)
            time.sleep(0.5)
            print(len(all_models))

        return all_models

    def get_model_info_by_id(self, model_id):
        endpoint = f"/api/models/{model_id}"
        headers = {"authorization": "Bearer {}".format(self.api_key)}

        response = requests.get(self.base_url + endpoint, headers=headers)
        
        response_dict = json.loads(response.content)

        return response_dict

    def get_dataset_list(self, keyword=None):
        endpoint = "/api/datasets"
        query_params = {"search": keyword if isinstance(keyword, str) else ""}
        response = requests.get(self.base_url + endpoint, query_params)
        response_dict = json.loads(response.content)

        return response_dict
    
    def get_dataset_by_id(self, dataset_id):
        endpoint = f"/api/datasets/{dataset_id}"
        headers = {"authorization": "Bearer {}".format(self.api_key)}
        response = requests.get(self.base_url + endpoint, headers=headers)
        response_dict = json.loads(response.content)

        return response_dict



def save_json(hf_api, save_dir, keyword):
    # dataset
    dataset_list = hf_api.get_dataset_list(keyword=keyword)
    with open(f'{save_dir}/dataset_list.json', 'w') as f:
        json.dump(dataset_list, f, indent=4)

    # models with "code" keywords
    model_list = hf_api.get_model_list_by_keywords(keyword)
    print(len(model_list))
    # save the model list
    with open(f'{save_dir}/model_list_{keyword}.json', 'w') as f:
        json.dump(model_list, f, indent=4)
    
    return


    # detail information of each model
    model_detail_dict = {}
    count = 0
    for model in model_list:
        modelId = model['modelId']
        try:
            model_info = hf_api.get_model_info_by_id(modelId)
        except:
            print(f'Error: {modelId}')
            continue

        # add model info to dict
        model_detail_dict[modelId] = model_info
        time.sleep(0.1)
        count += 1
        print('.', end='')
        if count % 100 == 0:
            print(f'Finished {count} models')

    # save model info dict
    with open(f'{save_dir}/model_detail_dict_{keyword}.json', 'w') as f:
        json.dump(model_detail_dict, f, indent=4)


def save_csv(save_dir, keyword):
    # read json file
    with open(f'{save_dir}/model_detail_dict_{keyword}.json', 'r') as f:
        model_detail_dict = json.load(f)
    
    # save csv file
    import csv
    with open(f'{save_dir}/model_dependency_{keyword}.csv', 'w') as f:
        # header: Model Name
        f.write('Model Name,\n')

        # write model
        model_list = list(model_detail_dict.keys())
        for model in model_list:
            f.write(f'{model},\n')


def snowballing_from_data_to_model(hf_api):
    file_path = 'data/data-data_dependency.csv'
    data_set = set()
    with open(file_path, 'r', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            data_set.add(row[0])
            data_set.add(row[1])

    # obtain models that dependent on the data
    for data in data_set:
        if len(data) < 3:
            continue
        data_list = hf_api.get_dataset_by_id(data)
        print(data)
        print(data_list)




if __name__ == '__main__':

    save_dir = 'major_revision'
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    # obtain API Key
    api_key = config['huggingface_key']
    hf_api = HuggingFaceAPI(api_key)


    # snowballing_from_data_to_model(hf_api)
    
    # 'python', 'java', 'py', 'rust', 'ruby', 'c++', 'c#', 'javascript',
    keyword_list = ['php', 'swift']
    for keyword in keyword_list:
        print(keyword)
        save_json(hf_api, save_dir, keyword=keyword)


    exit()
    save_csv(save_dir='data', keyword=keyword)

    exit()

    # transform data list to json
    with open(f'{save_dir}/dataset_list.json', 'r') as f:
        dataset_list = json.load(f)
    
    dataset_dict = {}
    for dataset in dataset_list:
        datasetId = dataset['id']
        dataset_dict[datasetId] = dataset

    with open(f'{save_dir}/dataset_dict.json', 'w') as f:
        json.dump(dataset_dict, f, indent=4)
        
