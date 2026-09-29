from fastapi import FastAPI
from pydantic import BaseModel

from database import (
    initialize_database,
    insert_metric,
    get_all_metrics,
    get_latest_metric,
    insert_alert,
    get_all_alerts
)

from health import evaluate_health

from alerts import(
    should_alert,
    create_alert_message
)

from notifier import send_notification


app = FastAPI()

initialize_database()

class TelemetryRecord(BaseModel):
    hostname: str
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float


@app.get("/")
def root():
    return {"message": "Telemetry server is running"}


@app.post("/metrics")
def receive_metrics(metrics: TelemetryRecord):
    metric_data = metrics.model_dump()

    previous_metric = get_latest_metric(
        metrics.hostname
    )

    previous_status = None

    if previous_metric is not None:
        previous_health = evaluate_health(
            previous_metric
        )

        previous_status = previous_health["overall"]

    current_health = evaluate_health(metric_data)
    current_status = current_health["overall"]

    insert_metric(metric_data)

    alert_message = None

    if should_alert(previous_status, current_status):
        alert_message = create_alert_message(
            metrics.hostname,
            current_health
        )

        alert_data = {
            "hostname": metrics.hostname,
            "timestamp": metric_data["timestamp"],
            "severity": current_status,
            "message": alert_message
        }

        insert_alert(alert_data)

        if current_status == "critical":
            send_notification(
                "Critical Machine Alert",
                alert_message
            )

        print("ALERT:", alert_message)

    return {
        "status": "received",
        "hostname": metrics.hostname,
        "health": current_health,
        "alert": alert_message
    }


@app.get("/metrics")
def get_metrics():
    return get_all_metrics()

"""
@app.get("/metrics/{hostname}")
def get_metrics_by_hostname(hostname: str):
    results = []

    for metric in telemetry_store:
        if metric["hostname"] == hostname:
            results.append(metric)

    return results

"""

@app.get("/health/{hostname}")
def get_health(hostname: str):
    metric = get_latest_metric(hostname)

    if metric is None:
        return {
            "status": "unknown",
            "message": "No telemetry found for this machine"
        }

    health = evaluate_health(metric)

    return {
        "hostname": hostname,
        "timestamp": metric["timestamp"],
        "health": health
    }


@app.get("/alerts")
def get_alerts():
    return get_all_alerts()