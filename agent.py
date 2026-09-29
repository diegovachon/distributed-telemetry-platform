import time
from collector import collect_system_metrics

import requests

from config import(
    COLLECTION_INTERVAL,
    SERVER_URL
)

def run_agent():
    try:
        while True:
            metrics = collect_system_metrics()

            print(metrics)

            response = send_metrics(metrics)

            if response is not None:
                print("Server response:", response.status_code)
                print("Response body:", response.text)

            time.sleep(COLLECTION_INTERVAL)

    except KeyboardInterrupt:
        print("Telemetry agent stopped.")


def send_metrics(metrics):
    try:
        response = requests.post(
            SERVER_URL,
            json=metrics,
            timeout=COLLECTION_INTERVAL
        )

        return response

    except requests.RequestException as error:
        print("Failed to send telemetry:", error)

        return None

if __name__ == "__main__":
    run_agent()