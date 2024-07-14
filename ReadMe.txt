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
    ```sh
    git clone https://github.com/MarkoPolo15/SAM_seamless_network.git
    cd SAM_seamless_network
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    ```


3. **Install Dependencies**:
    ```
    pip install -r requirements.txt
    ```

4. **Create a `.env` File**:
    If diesnt exist - Create a `.env` file in the project root directory and add the following environment variables:
    ```plaintext
    API_URL=https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking/
    AUTH_TOKEN=I_am_under_stress_when_I_test
    ```

## Usage

1. **Run the `run_stress_test.py` Script**:
    ```sh
    python run_stress_test.py --concurrent_requests 10 --number_of_domains 100 --timeout 60 --output results.csv --retry 3 --verbose --use_retries
    ```

    ### Arguments:
    - `--concurrent_requests`: Number of concurrent requests.
    - `--number_of_domains`: Total number of domain requests (max: 5000).
    - `--timeout`: Timeout in seconds.
    - `--output`: Output CSV file name.
    - `--retry`: Number of retries for failed requests.
    - `--verbose`: Enable verbose mode for more detailed output.
    - `--use_retries`: Use retries for requests.
