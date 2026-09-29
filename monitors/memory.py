import psutil


def collect():
    memory = psutil.virtual_memory()

    return {
        "memory_percent": memory.percent
    }