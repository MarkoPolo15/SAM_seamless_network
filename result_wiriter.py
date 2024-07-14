import csv
import logging
from datetime import datetime
from statistics_calculator import StatisticsCalculator

class ResultWriter:
    def __init__(self, output):
        self.output = output

    def print_results(self, responses, total_time, reason):
        calculator = StatisticsCalculator()

        total_requests = len(responses)
        failed_requests = []
        durations = []

        for domain, response in responses:
            if response.status_code != 200:
                failed_requests.append(response)
            else:
                durations.append(response.elapsed.total_seconds())

        average_duration, max_duration, p90_duration = calculator.calculate_statistics(durations)
        error_rate = calculator.calculate_error_rate(failed_requests, total_requests)
        requests_per_second = calculator.calculate_requests_per_second(total_requests, total_time)
        status_code_counts = calculator.get_status_code_counts(responses)

        logging.info("Test is over!")
        logging.info(f"Reason: {reason}")
        logging.info(f"Time in total: {total_time:.0f} seconds")
        logging.info(f"Requests in total: {total_requests}")
        logging.info(f"Error rate: {error_rate:.0f}% ({len(failed_requests)} / {total_requests})")
        logging.info(f"Average time for one request: {average_duration * 1000:.1f} ms")
        logging.info(f"Max time for one request: {max_duration:.1f} seconds")
        logging.info(f"P90 time for one request: {p90_duration:.1f} seconds")
        logging.info(f"Requests per second: {requests_per_second:.2f} RPS")

        logging.info("HTTP status code breakdown:")
        for status_code, count in status_code_counts.items():
            percentage = (count / total_requests) * 100 if total_requests else 0
            logging.info(f"  {status_code}: {count} ({percentage:.0f}%)")

        self.write_results_to_csv(responses, total_time, total_requests, error_rate, average_duration, max_duration, p90_duration, requests_per_second, status_code_counts)

    def write_results_to_csv(self, responses, total_time, total_requests, error_rate, average_duration, max_duration, p90_duration, requests_per_second, status_code_counts):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{self.output}_{timestamp}.csv"
        logging.info(f"Writing results to {output_filename}")

        try:
            with open(output_filename, "w", newline="") as csvfile:
                fieldnames = ["domain", "duration", "status", "error"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for domain, response in responses:
                    writer.writerow({
                        "domain": domain,
                        "duration": response.elapsed.total_seconds(),
                        "status": "success" if response.status_code == 200 else "failed",
                        "error": response.status_code if response.status_code != 200 else ""
                    })

                # Write summary statistics at the end of the CSV
                writer.writerow({})
                writer.writerow({"domain": "Summary"})
                writer.writerow({"domain": "Total time", "duration": total_time})
                writer.writerow({"domain": "Total requests", "duration": total_requests})
                writer.writerow({"domain": "Error rate", "duration": f"{error_rate:.0f}%"})
                writer.writerow({"domain": "Average duration", "duration": average_duration})
                writer.writerow({"domain": "Max duration", "duration": max_duration})
                writer.writerow({"domain": "P90 duration", "duration": p90_duration})
                writer.writerow({"domain": "Requests per second (RPS)", "duration": requests_per_second})

                for status_code, count in status_code_counts.items():
                    percentage = (count / total_requests) * 100 if total_requests else 0
                    writer.writerow({"domain": f"HTTP {status_code}", "duration": count, "status": f"{percentage:.0f}%"})

            logging.info("Results successfully written to CSV")
        except Exception as e:
            logging.error(f"An error occurred while writing to CSV: {e}")
