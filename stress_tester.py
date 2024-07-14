import time
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
from domain_fetcher import DomainFetcher
from request_creator import RequestCreator
from result_wiriter import ResultWriter

class StressTester:
    def __init__(self, concurrent_requests, number_of_domains, timeout, output, retries, verbose, use_retries):
        self.concurrent_requests = concurrent_requests
        self.number_of_domains = number_of_domains
        self.timeout = timeout
        self.output = output
        self.retries = retries
        self.verbose = verbose
        self.use_retries = use_retries
        self.api_url = os.getenv("API_URL")
        self.auth_token = os.getenv("AUTH_TOKEN")
        if not self.auth_token:
            raise ValueError("AUTH_TOKEN is not set in the environment variables")
        self.domain_fetcher = DomainFetcher(self.number_of_domains)
        self.request_handler = RequestCreator(self.api_url, self.auth_token, retries, verbose)
        self.result_writer = ResultWriter(output)

        if self.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.info("Verbose mode enabled")

    def _wrap_request(self, domain):
        if self.use_retries:
            return self.request_handler.create_request_with_retries(domain)
        else:
            return self.request_handler.create_request(domain)

    def run(self):
        domains = self.domain_fetcher.get_domains()
        domain_cycle = cycle(domains)
        responses = []
        start_time = time.time()
        completed_requests = 0
        interrupted = False

        try:
            logging.info(f"Starting stress test with {self.concurrent_requests} concurrent requests")

            with ThreadPoolExecutor(max_workers=self.concurrent_requests) as executor:
                request_to_domain = {}
                for _ in range(min(self.concurrent_requests, self.number_of_domains)):
                    domain = next(domain_cycle)
                    request = executor.submit(self._wrap_request, domain)
                    request_to_domain[request] = domain

                while completed_requests < self.number_of_domains:
                    for request in as_completed(request_to_domain):
                        try:
                            response = request.result()
                            responses.append((request_to_domain[request], response))
                            completed_requests += 1

                            if completed_requests < self.number_of_domains:
                                domain = next(domain_cycle)
                                new_request = executor.submit(self._wrap_request, domain)
                                request_to_domain[new_request] = domain
                        except Exception as e:
                            logging.error(f"An error occurred: {e}")
                        finally:
                            del request_to_domain[request]

                        if completed_requests >= self.number_of_domains:
                            break

                        if time.time() - start_time > self.timeout:
                            interrupted = True
                            break

        except KeyboardInterrupt:
            interrupted = True
            reason = "keyboard interrupt"
        else:
            reason = "timeout" if interrupted else "completed"

        finally:
            end_time = time.time()
            total_time = end_time - start_time
            self.result_writer.print_results(responses, total_time, reason if interrupted else "completed")
