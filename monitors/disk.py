import psutil


def collect():
    disk = psutil.disk_usage("/")

    return {
        "disk_percent": disk.percent
    }