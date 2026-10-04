import pandas as pd
import time
import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.playbook_rules import generate_playbook


DATA_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "clean_soc_cases.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "performance_results.csv"
)


def main():

    print("=" * 60)
    print("SOC PLAYBOOK ASSISTANT - PERFORMANCE TEST")
    print("=" * 60)

    df = pd.read_csv(DATA_FILE)

    test_cases = df.head(100).to_dict("records")

    response_times = []

    print(f"\nTest Cases : {len(test_cases)}")
    print("Running performance test...\n")

    for case in test_cases:

        start_time = time.perf_counter()

        generate_playbook(case)

        end_time = time.perf_counter()

        response_time_ms = (
            end_time - start_time
        ) * 1000

        response_times.append(response_time_ms)

    average_time = (
        sum(response_times) /
        len(response_times)
    )

    minimum_time = min(response_times)
    maximum_time = max(response_times)

    sorted_times = sorted(response_times)

    p95_index = int(
        0.95 * len(sorted_times)
    ) - 1

    p95_time = sorted_times[
        max(0, p95_index)
    ]

    print("=" * 60)
    print("PERFORMANCE RESULTS")
    print("=" * 60)

    print(
        f"Average Response Time : "
        f"{average_time:.4f} ms"
    )

    print(
        f"Minimum Response Time : "
        f"{minimum_time:.4f} ms"
    )

    print(
        f"Maximum Response Time : "
        f"{maximum_time:.4f} ms"
    )

    print(
        f"95th Percentile       : "
        f"{p95_time:.4f} ms"
    )

    target_ms = 1000

    status = (
        "PASS"
        if average_time <= target_ms
        else "BELOW TARGET"
    )

    print(
        f"\nTarget Response Time  : "
        f"< {target_ms} ms"
    )

    print(
        f"Performance Status    : {status}"
    )

    results = pd.DataFrame({
        "metric": [
            "Test Cases",
            "Average Response Time (ms)",
            "Minimum Response Time (ms)",
            "Maximum Response Time (ms)",
            "95th Percentile (ms)",
            "Target Response Time (ms)",
            "Status"
        ],
        "value": [
            len(test_cases),
            round(average_time, 4),
            round(minimum_time, 4),
            round(maximum_time, 4),
            round(p95_time, 4),
            target_ms,
            status
        ]
    })

    results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nResults saved to:")
    print(OUTPUT_FILE)

    print(
        "\nPerformance testing "
        "completed successfully."
    )


if __name__ == "__main__":
    main()
