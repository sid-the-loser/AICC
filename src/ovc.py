import requests
import json

def get_online_version_using_json(url: str, lookup_pattern:list[str], timeout:float = None) -> str:
    online_version = None

    try:
        with requests.get(url=url, timeout=timeout) as data:
            temp = json.loads(data.content)

            for string in lookup_pattern:
                temp = temp[string]

            online_version = str(temp)
    except:
        online_version = None

    return online_version