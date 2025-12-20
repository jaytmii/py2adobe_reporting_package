"""This module covers all authentication methods"""
import json
import requests
# from authlib.integrations.requests_client import OAuth2Session


## Integration format
# {
#     "clientSecret": "clientSecretVal",
#     "companyId": "companyIdVal",
#     "imsHost": "ims-na1.adobelogin.com",
#     "tokenUrl": "/ims/token/v3",
#     "defaultHeaders": {
#         "Accept": "application/json",
#         "x-api-key": "apiKey",
#         "x-gw-ims-org-id": "orgIdVal"
#     },
#     "scopes": "scopes by area comma delimited"
# }
class TokenURL():
    """To store your token URL components"""
    def __init__(self, imsHost, tokenUrl):
        self.imsHost = imsHost
        self.tokenUrl = tokenUrl

    def get_token_url(self):
        """function to get token url from config"""
        url_full = f"https://{self.imsHost}{self.tokenUrl}"
        return url_full
        


def json_load(your_config_file):
    """Loading function for json integration file format"""
    try:
        with open(your_config_file, "r", encoding="utf-8") as file:
            config_json = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found.")
    except json.JSONDecodeError:
        raise Exception("Config file is invalid - ensure JSON formatting is correct.")
    return config_json

def get_config_values(config_json):
    """Function to extract and return values from the config file."""
    headers = config_json.get('defaultHeaders')
    return headers, {
            "apiKey": headers.get('x-api-key') if headers else None,
            "orgId": headers.get('x-gw-ims-org-id') if headers else None,
            "companyId": config_json.get('companyId'),
            "clientSecret": config_json.get('clientSecret'),
            # "apiName": config_json.get('name'),
            "scopes": config_json.get('scopes')
            }

## Tool specific header functions
def cja_oauth_headers(your_config_file, access_token):
    """CJA Specific headers"""
    config_json = json_load(your_config_file)
    headers, config_values = get_config_values(config_json)
    cja_headers = {
    "Content-Type" : "application/json",
    "Accept" : "application/json",
    "x-gw-ims-org-id": config_values['orgId'],
    "x-api-key" : config_values['apiKey'],
    "Authorization" : "Bearer " + access_token}
    return cja_headers

def aep_oauth_headers(your_config_file, access_token, accept_header, sandbox):
    """AEP specific headers"""
    config_json = json_load(your_config_file)
    headers, config_values = get_config_values(config_json)
    aep_headers = {
    "Content-Type" : "application/json",
    "Accept" : accept_header,
    "x-gw-ims-org-id": config_values['orgId'],
    "x-sandbox-name": sandbox,
    "x-api-key" : config_values['apiKey'],
    "Authorization" : "Bearer " + access_token}
    return aep_headers

class aepEnv:
    """To store your authentication credentials"""
    def __init__(self, apiKey, orgId, companyId, token):
        self.apiKey = apiKey
        self.orgId = orgId
        self.companyId = companyId
        self.token = token

def s2sAuth(
    filename
):
    """Primary S2S Auth function"""
    config_json = json_load(filename)
    headers, config_values = get_config_values(config_json)

    print(f"Authenticating using file: {filename}")

    tokenUrlFull = TokenURL(config_json.get("imsHost"), config_json.get("tokenUrl")).get_token_url()
    payload = {
        'client_id': config_values['apiKey'],
        'client_secret': config_values['clientSecret'],
        'grant_type': 'client_credentials',
        'scope': config_values['scopes']
    }

    response = requests.post(tokenUrlFull, data=payload, timeout = 10)
    if response.status_code == 200:
        token = response.json()
        print(token['access_token'])
        return aepEnv(config_values['apiKey'], config_values['orgId'], config_values['companyId'], token['access_token'])
    else:
        raise requests.exceptions.RequestException(f"Failed to authenticate. Status code: {response.status_code}, Response: {response.text}")
