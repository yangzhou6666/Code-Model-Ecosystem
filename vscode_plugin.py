import json
import requests

url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"

payload = {
    "filters": [{
        "criteria": [{
            "filterType": 8,
            "value": "Microsoft.VisualStudio.Code"
        }, {
            "filterType": 10,
            "value": "AI"
        }]
    }],
    "flags": 870
}

response = requests.post(url, json=payload)

data = response.json()




# 打印出所有的扩展信息
for extension in data["results"][0]["extensions"]:
    # print(extension["extensionName"], extension["publisher"]["publisherName"])
    print(json.dumps(extension, indent=4))
print(len(data["results"][0]["extensions"]))