"""This module covers all authentication methods"""
import json
import requests
# from authlib.integrations.requests_client import OAuth2Session


## Integration format
# {
#     "client_secret": "clientSecretVal",
#     "company_id": "companyIdVal",
#     "ims_host": "ims_host_val",
#     "token_url": "token_url_val",
#     "default_headers": {
#         "Accept": "application/json",
#         "x-api-key": "apiKey",
#         "x-gw-ims-org-id": "orgIdVal"
#     },
#     "scopes": "scopes by area comma delimited"
# }
class TokenURL():
    """To store your token URL components"""
    def __init__(self, ims_host, token_url):
        self.ims_host = ims_host
        self.token_url = token_url

    def get_token_url(self):
        """function to get token url from config"""
        url_full = f"https://{self.ims_host}{self.token_url}"
        return url_full


def json_load(your_config_file):
    """Loading function for json integration file format"""
    try:
        with open(your_config_file, "r", encoding="utf-8") as file:
            config_json = json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError("Config file not found.") from exc
    except json.JSONDecodeError as exc:
        raise Exception("Config file is invalid - ensure JSON formatting is correct.") from exc
    return config_json

def get_config_values(config_json):
    """Function to extract and return values from the config file."""
    headers = config_json.get('default_headers')
    return headers, {
            "api_key": headers.get('x-api-key') if headers else None,
            "org_id": headers.get('x-gw-ims-org-id') if headers else None,
            "company_id": config_json.get('company_id'),
            "client_secret": config_json.get('client_secret'),
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
    "x-gw-ims-org-id": config_values['org_id'],
    "x-api-key" : config_values['api_key'],
    "Authorization" : "Bearer " + access_token}
    return cja_headers

def aep_oauth_headers(your_config_file, access_token, accept_header, sandbox):
    """AEP specific headers"""
    config_json = json_load(your_config_file)
    headers, config_values = get_config_values(config_json)
    aep_headers = {
    "Content-Type" : "application/json",
    "Accept" : accept_header,
    "x-gw-ims-org-id": config_values['org_id'],
    "x-sandbox-name": sandbox,
    "x-api-key" : config_values['api_key'],
    "Authorization" : "Bearer " + access_token}
    return aep_headers

class AEPEnv:
    """To store your authentication credentials"""
    def __init__(self, api_key, org_id, company_id, token):
        self.api_key = api_key
        self.org_id = org_id
        self.company_id = company_id
        self.token = token

def s2s_auth(
    filename
):
    """Primary S2S Auth function"""
    config_json = json_load(filename)
    headers, config_values = get_config_values(config_json)

    print(f"Authenticating using file: {filename}")

    token_url_full = TokenURL(config_json.get("ims_host"), config_json.get("token_url")).get_token_url()
    payload = {
        'client_id': config_values['api_key'],
        'client_secret': config_values['client_secret'],
        'grant_type': 'client_credentials',
        'scope': config_values['scopes']
    }

    response = requests.post(token_url_full, data=payload, timeout = 10)
    if response.status_code == 200:
        token = response.json()
        print(token['access_token'])
        return AEPEnv(config_values['api_key'],
                      config_values['org_id'],
                      config_values['company_id'],
                      token['access_token'])
    else:
        raise requests.exceptions.RequestException(f"Failed to authenticate. Status code: {response.status_code}, Response: {response.text}")
