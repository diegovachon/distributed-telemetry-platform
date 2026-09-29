import psutil


def collect():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1)
    }