"""Repporting API endpoints, base urls, and error handling"""

# from py2AdobeReporting.cja_functions.reporting_management import Reporting

class ReportingAPI:
    """Class for all Reporting API related functionality"""
    BASE_URL = "https://cja.adobe.io/reports"
    TOP_ITEMS_ENDPOINT = "/topItems"

    @classmethod
    def base_url(cls):
        """The base url for the reporting API"""
        return cls.BASE_URL
    
    @classmethod
    def get_top_items_endpoint(cls):
        """The endpoint for top items"""
        return cls.TOP_ITEMS_ENDPOINT

    @classmethod    
    def build_url(cls, endpoint):
        """Builds the full URL for a given endpoint"""
        return f"{cls.BASE_URL}{endpoint}"

    @classmethod
    def build_get_top_items_url(cls):
        """Builds the full URL for the top items endpoint"""
        return f"{cls.BASE_URL}{cls.TOP_ITEMS_ENDPOINT}"
    
    class SuccessfullResponseCodes:
        """Class for handling successful response codes"""
        default_message = "Successful Response"
        def __init__(self, message=None):
            self.message = message or self.default_message

        def __str__(self):
            return self.message
        
    class JsonConversionFailure(Exception):
        """When a call is succesful but json conversion fails for parsing"""
        default_message = "API Call returned succesfully, but JSON conversion failed."

    class SuccessfulOK(SuccessfullResponseCodes):
        """200 status code response"""
        default_message = "OK"

    class SuccessfulAccepted(SuccessfullResponseCodes):
        """202 status code response"""
        default_message = "Accepted. Details returned in response body."

    class ClientError(Exception):
        """Base exception for all CJA Reporting API error codes"""
        default_message = "CJA Reporting API error"
        def __init__(self, message=None):
            super().__init__(message or self.default_message)
            
    class MalformedRequest(ClientError):
        """400 status code response"""
        default_message = "Malformed Request"

    class UnauthorizedRequest(ClientError):
        """401 status code response"""
        default_message = "Unauthorized Request"
        
    class ForbiddenRequest(ClientError):
        """403 status code response"""
        default_message = "Forbidden Request"

    class ResourceNotFound(ClientError):
        """404 status code response"""
        default_message = "Resource Not Found"
        
    class InternalServerError(ClientError):
        """500 status code response"""
        default_message = "Internal Server Error"

    def status_handling(self, response_object):
        code_dict = {
            200: self.SuccessfulOK,
            202: self.SuccessfulAccepted,
            400: self.MalformedRequest,
            401: self.UnauthorizedRequest,
            403: self.ForbiddenRequest,
            404: self.ResourceNotFound,
            500: self.InternalServerError,
        }
        try:
            status_code = response_object.status_code
        except:
            raise self.ClientError("Response object is not formatted correctly")
        error_exc = code_dict.get(status_code)
        if status_code < 300:
            success = code_dict.get(status_code, self.SuccessfullResponseCodes)
            return str(success())
        if error_exc is None:
            if 400 <= status_code < 500:
                error_exc = self.ClientError
            elif 500 <= status_code < 600:
                error_exc = self.InternalServerError
            else:
                return "Unknown Status Code Response"
        raise error_exc()