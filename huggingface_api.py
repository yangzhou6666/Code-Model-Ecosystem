'''play with huggingface API to obtain some information'''

import requests
import json
import yaml

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
        endpoint = f"/api/models/{repo_id}"
        headers = {"authorization": "Bearer {}".format(self.api_key)}

        response = requests.get(base_url + endpoint, headers=headers)
        response_dict = json.loads(response.content)

        return response_dict


if __name__ == '__main__':
    with open('config.yaml') as f:
        config = yaml.load(f)
    # obtain API Key
    api_key = config['huggingface_key']

    hf_api = HuggingFaceAPI(api_key)
    model_list = hf_api.get_model_list_by_keywords("code")
    print(len(model_list))