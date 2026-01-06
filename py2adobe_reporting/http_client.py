"""Module for API Call functionality improvements"""
import time
import requests
from py2adobe_reporting.reporting_api import ReportingAPI

## Use the following syntax for different calls ##
# GET CALL: HttpClient(url,headers).get()
# POST CALL: HttpClient(url,headers,req_num,payload_type,body).post()
# PUT CALL: HttpClient(url,headers,req_num,payload_type,body).put()
# DELETE CALL: HttpClient(url,headers).delete()
# PATCH CALL: HttpClient(url, headers, req_num, payload_type, body).patch()

# Constants
TIMEOUT = 300
DEFAULT_RETRY_COUNT = 5
RETRY_DELAY = 5
SUCCESS_CODES = (200, 202)

class HttpClient(ReportingAPI):
    """Class converting all API call functionality for the package"""
    def __init__(self,
                 url,
                 headers,
                 req_num = 5,
                 payload_type = '',
                 body=None):
        self.url = url
        self.headers = headers
        self.req_num = req_num
        self.body = body
        self.payload_type = payload_type

    def type_of_api_call(self,
                         type_of_call):
        """This is to identify formatting for the call"""
        req_payload = {
            "url": self.url,
            "headers": self.headers,
            "timeout": TIMEOUT
        }
        if self.payload_type == "json" and self.body is not None:
            req_payload["json"] = self.body
        elif self.payload_type == "params" and self.body is not None:
            req_payload["params"] = self.body
        elif self.payload_type == "data" and self.body is not None:
            req_payload["data"] = self.body
        try:
            return requests.request(type_of_call, **req_payload)
        except requests.exceptions.HTTPError as error:
            print("Wrongly specified Call Type: ", error)

    def api_retry(self, type_of_call, req_num=5):
        """This provides logic for when a call will be tried again, how much, and error handling"""
        attempt_count = 0
        print("API Request Number " + str(attempt_count + 1))
        initial_response = self.type_of_api_call(type_of_call)
        print("Status Code: " + str(initial_response.status_code))
        attempt_count+=1
        if initial_response.status_code in SUCCESS_CODES:
            print(self.status_handling(initial_response))
            return initial_response
        else:
            print("Initial call was unsuccesful. Retry in 5 seconds...")
            while attempt_count < req_num:
                time.sleep(RETRY_DELAY)
                print("API Request Number " + str(attempt_count + 1))
                retry_response = self.type_of_api_call(type_of_call)
                print("Status Code: " + str(retry_response.status_code))
                if retry_response.status_code in SUCCESS_CODES:
                    print(self.status_handling(retry_response))
                    return retry_response
                else:
                    print(self.status_handling(retry_response))
                    print("Trying API call again in 5 seconds....")
                attempt_count+=1
        print(f"API call failed after {req_num} attempts.")
        return None

    def get(self):
        """Class function for GET Calls incorporating retry script"""
        type_of_call = "GET"
        res = self.api_retry(type_of_call, self.req_num)
        return res

    def post(self):
        """Class function for POST Calls incorporating retry script"""
        type_of_call = "POST"
        res = self.api_retry(type_of_call, self.req_num)
        return res

    def put(self):
        """Class function for PUT Calls incorporating retry script"""
        type_of_call = "PUT"
        res = self.api_retry(type_of_call, self.req_num)
        return res

    def patch(self):
        """Class function for PATCH Calls incorporating retry script"""
        type_of_call = "PATCH"
        res = self.api_retry(type_of_call, self.req_num)
        return res

    def delete(self):
        """Class function for DELETE Calls incorporating retry script"""
        type_of_call = "DELETE"
        res = self.api_retry(type_of_call, self.req_num)
        return res

