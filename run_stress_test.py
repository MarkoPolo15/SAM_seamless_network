import argparse
import os
import logging
from dotenv import load_dotenv
from stress_tester import StressTester

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Configure logging to show only INFO and higher level messages
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="Simulate stress on Reputation service")
    parser.add_argument("--concurrent_requests", type=int, required=True, help="Number of concurrent requests")
    parser.add_argument("--number_of_domains", type=int, required=True, help="Total number of domain requests (max: 5000)")
    parser.add_argument("--timeout", type=int, required=True, help="Timeout in seconds")
    parser.add_argument("--output", type=str, default="results.csv", help="Output CSV file name")
    parser.add_argument("--retry", type=int, default=3, help="Number of retries for failed requests")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose mode for more detailed output")
    parser.add_argument("--use_retries", action='store_true', help="Use retries for requests")

    args = parser.parse_args()

    if args.number_of_domains > 5000:
        print("The number of domains should not exceed 5000.")
        return

    # Create the test_output/csv directory if it doesn't exist
    output_directory = os.path.join("test_output", "csv")
    os.makedirs(output_directory, exist_ok=True)

    # Create the full output path
    output_path = os.path.join(output_directory, args.output)

    tester = StressTester(
        concurrent_requests=args.concurrent_requests,
        number_of_domains=args.number_of_domains,
        timeout=args.timeout,
        output=output_path,
        retries=args.retry,
        verbose=args.verbose,
        use_retries=args.use_retries
    )
    tester.run()

if __name__ == "__main__":
    main()
