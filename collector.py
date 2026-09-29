import psutil
import socket
from datetime import datetime, timezone

from monitors import cpu
from monitors import memory
from monitors import disk

MONITORS = [
    cpu,
    memory,
    disk
]

def collect_system_metrics():
    metrics = {
        "hostname": socket.gethostname()
    }

    for monitor in MONITORS:
        monitor_metrics = monitor.collect()

        metrics.update(monitor_metrics)

    metrics["timestamp"] = (
        datetime.now(timezone.utc).isoformat()
    )

    return metrics
