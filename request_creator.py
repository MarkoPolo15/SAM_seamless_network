import requests
import logging

class RequestCreator:
    def __init__(self, api_url, auth_token, retries=3, verbose=False):
        self.api_url = api_url
        self.auth_token = auth_token
        self.retries = retries
        self.verbose = verbose

    def create_request(self, domain):
        url = f"{self.api_url}{domain}"
        headers = {"Authorization": f"Token {self.auth_token}"}
        return requests.get(url, headers=headers)

    def create_request_with_retries(self, domain):
        for attempt in range(self.retries):
            response = self.create_request(domain)
            if response.status_code == 200:
                return response
            if self.verbose:
                logging.info(f"Retry {attempt + 1} for domain {domain}")
        return response
