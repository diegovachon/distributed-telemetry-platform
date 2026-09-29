import os


COLLECTION_INTERVAL = int(
    os.getenv("COLLECTION_INTERVAL", "60")
)

SERVER_URL = os.getenv(
    "SERVER_URL",
    "http://127.0.0.1:8000/metrics"
)


CPU_WARNING = float(
    os.getenv("CPU_WARNING", "80")
)

CPU_CRITICAL = float(
    os.getenv("CPU_CRITICAL", "90")
)


MEMORY_WARNING = float(
    os.getenv("MEMORY_WARNING", "80")
)

MEMORY_CRITICAL = float(
    os.getenv("MEMORY_CRITICAL", "90")
)


DISK_WARNING = float(
    os.getenv("DISK_WARNING", "80")
)

DISK_CRITICAL = float(
    os.getenv("DISK_CRITICAL", "90")
)