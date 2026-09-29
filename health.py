"""
Interpret raw telemetry and determine machine health
"""
from config import(
    CPU_WARNING,
    CPU_CRITICAL,
    MEMORY_CRITICAL,
    MEMORY_WARNING,
    DISK_CRITICAL,
    DISK_WARNING
)

def evaluate_metric(value, warning_threshold, critical_threshold):
    if value >= critical_threshold:
        return "critical"

    if value >= warning_threshold:
        return "warning"

    return "healthy"


def evaluate_health(metrics):
    cpu_status = evaluate_metric(
        metrics["cpu_percent"],
        CPU_WARNING,
        CPU_CRITICAL
    )

    memory_status = evaluate_metric(
        metrics["memory_percent"],
        MEMORY_WARNING,
        MEMORY_CRITICAL
    )

    disk_status = evaluate_metric(
        metrics["disk_percent"],
        DISK_WARNING,
        DISK_CRITICAL
    )

    statuses = [
        cpu_status,
        memory_status,
        disk_status
    ]
    overall_status = determine_overall_status(statuses)

    return {
        "overall": overall_status,
        "cpu": cpu_status,
        "memory": memory_status,
        "disk": disk_status
    }


def determine_overall_status(statuses):
    if "critical" in statuses:
        return "critical"

    if "warning" in statuses:
        return "warning"

    return "healthy"