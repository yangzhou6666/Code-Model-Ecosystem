'''play with huggingface API to obtain some information'''

import requests
import json
import yaml
import time

class HuggingFaceAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://huggingface.co"
        self.interval = 0.5 # seconds

    def set_interval(self, interval):
        self.interval = interval

    def get_model_list_by_keywords(self, keyword=None):
        endpoint = "/api/models"
        query_params = {"search": keyword if isinstance(keyword, str) else ""}
        response = requests.get(self.base_url + endpoint, query_params)
        response_dict = json.loads(response.content)

        return response_dict

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


def save_json(hf_api, save_dir):
    # dataset
    dataset_list = hf_api.get_dataset_list()
    with open(f'{save_dir}/dataset_list.json', 'w') as f:
        json.dump(dataset_list, f, indent=4)

    # models with "code" keywords
    model_list = hf_api.get_model_list_by_keywords("code")


    # detail information of each model
    model_detail_dict = {}
    count = 0
    for model in model_list:
        modelId = model['modelId']
        model_info = hf_api.get_model_info_by_id(modelId)

        # add model info to dict
        model_detail_dict[modelId] = model_info
        time.sleep(0.1)
        count += 1
        print('.', end='')
        if count % 100 == 0:
            print(f'Finished {count} models')

    # save model info dict
    with open(f'{save_dir}/model_detail_dict.json', 'w') as f:
        json.dump(model_detail_dict, f, indent=4)



if __name__ == '__main__':

    save_dir = 'data'
    with open('config.yaml') as f:
        config = yaml.load(f)
    # obtain API Key
    api_key = config['huggingface_key']

    hf_api = HuggingFaceAPI(api_key)

    # transform data list to json
    with open(f'{save_dir}/dataset_list.json', 'r') as f:
        dataset_list = json.load(f)
    
    dataset_dict = {}
    for dataset in dataset_list:
        datasetId = dataset['id']
        dataset_dict[datasetId] = dataset

    with open(f'{save_dir}/dataset_dict.json', 'w') as f:
        json.dump(dataset_dict, f, indent=4)
        
