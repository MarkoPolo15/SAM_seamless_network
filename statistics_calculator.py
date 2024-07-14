class StatisticsCalculator:
    def calculate_statistics(self, durations):
        if not durations:
            return 0, 0, 0

        average_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        p90_duration = sorted(durations)[int(len(durations) * 0.9)]

        return average_duration, max_duration, p90_duration

    def calculate_error_rate(self, failed_requests, total_requests):
        return len(failed_requests) / total_requests * 100 if total_requests else 0

    def calculate_requests_per_second(self, total_requests, total_time):
        return total_requests / total_time if total_time > 0 else 0

    def get_status_code_counts(self, responses):
        status_code_counts = {}
        for domain, response in responses:
            status_code_counts[response.status_code] = status_code_counts.get(response.status_code, 0) + 1
        return status_code_counts
