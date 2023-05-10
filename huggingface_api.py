'''play with huggingface API to obtain some information'''

import requests
import json
import yarm

class HuggingFaceAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://huggingface.co"
        self.interval = 0.5 # seconds

    def set_interval(self, interval):
        self.interval = interval

    def get_model_list_by_keywords(keyword=None):
        base_url = "https://huggingface.co"
        query_params = {"search": keyword if isinstance(keyword, str) else ""}
        response = requests.get(base_url + endpoint, query_params)
        model_list = json.loads(response.content)

        return model_list

    def get_model_info_by_id(self, model_id):
        endpoint = f"/api/models/{repo_id}"
        headers = {"authorization": "Bearer {}".format(self.api_key)}

        response = requests.get(base_url + endpoint, headers=headers)
        response_dict = json.loads(response.content)

        return response_dict


if __name__ == '__main__':
    with open('config.yaml') as f:
        config = yarm.load(f)
    # obtain API Key
    api_key = config['huggingface_key']