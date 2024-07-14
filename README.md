# Stress Test Tool

This project provides tools to perform stress testing on a list of domains and log the results.

## Project Structure
- `domain_fetcher.py`: Contains the `DomainFetcher` class to fetch a list of domains.
- `request_creator.py`: Contains the `RequestCreator` class to create and send HTTP requests.
- `result_writer.py`: Contains the `ResultWriter` class to process the responses and write the results to a CSV file.
- `run_stress_test.py`: Main script to run the stress test.
- `statistics_calculator.py`: Contains the `StatisticsCalculator` class with methods to calculate various statistics.
- `stress_tester.py`: Contains the `StressTester` class to orchestrate the stress test.
- `requirements.txt`: Lists the required Python libraries.
- `README.md`: This file with instructions and explanations.

## Setup

1. **Clone the Repository**:

    git clone https://github.com/MarkoPolo15/SAM_seamless_network.git
    cd SAM_seamless_network


2. **Create a Virtual Environment**:

    python -m venv venv



3. **Install Dependencies**:

    pip install -r requirements.txt


4. **Create a `.env` File**:
    If diesnt exist - Create a `.env` file in the project root directory and add the following environment variables:
    ```plaintext
    API_URL=https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking/
    AUTH_TOKEN=I_am_under_stress_when_I_test
    ```

## Usage

1. **Run the `run_stress_test.py` Script**:

    python run_stress_test.py --concurrent_requests 10 --number_of_domains 100 --timeout 60 --output results.csv --retry 3 --verbose --use_retries


    ### Arguments:
    - `--concurrent_requests`: Number of concurrent requests.
    - `--number_of_domains`: Total number of domain requests (max: 5000).
    - `--timeout`: Timeout in seconds.
    - `--output`: Output CSV file name.
    - `--retry`: Number of retries for failed requests.
    - `--verbose`: Enable verbose mode for more detailed output.
    - `--use_retries`: Use retries for requests.

2. **Example Output**:
    ```
    Test is over!
    Reason: timeout / keyboard interrupt
    Time in total: 38 seconds
    Requests in total: 45321
    Error rate: 23% (12345 / 45321)
    Average time for one request: 0.4 ms
    Max time for one request: 1.2 seconds
    ```

## Explanation of the Working Process

1. **Domain Fetching**:
    - The `DomainFetcher` class fetches a specified number of popular domains. The domains are cycled to ensure the specified number is met, even if domains are repeated.

2. **Request Creation**:
    - The `RequestCreator` class creates and sends HTTP requests to the Reputation service. It handles authentication and retries for failed requests.

3. **Stress Testing**:
    - The `StressTester` class orchestrates the stress test by managing concurrent requests using a thread pool. It collects responses and measures the time taken for each request.

4. **Result Writing**:
    - The `ResultWriter` class processes the responses, calculates statistics (average, max, and 90th percentile durations, error rate, requests per second, status code counts), and logs the results. It also writes detailed results to a CSV file.

5. **Statistics Calculation**:
    - The `StatisticsCalculator` class contains methods to calculate various statistics from the collected responses, such as average duration, max duration, 90th percentile duration, error rate, and requests per second.

6. **Handling Keyboard Interrupts**:
    - The tool handles `KeyboardInterrupt` exceptions to print intermediate results if the stress test is interrupted by the user.


