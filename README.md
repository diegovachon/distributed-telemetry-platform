# Distributed Telemetry Platform

Lightweight telemetry and health-monitoring platform built with Python, FastAPI, SQLite, and Docker.

It collects system metrics from agents, sends them to a centralized API, stores telemetry, evaluates machine health, and generates alerts when systems enter warning or critical states.

## Features

- CPU, memory, and disk monitoring
- Continuous telemetry collection
- REST API with FastAPI
- Persistent SQLite storage
- Health evaluation with configurable thresholds
- Warning and critical alert generation
- Environment-based configuration
- Modular monitoring components
- Docker and Docker Compose support

## Architecture

```text
Telemetry Agent
      |
      | HTTP / JSON
      v
 FastAPI Server
      |
      +----> SQLite
      |
      +----> Health Evaluation
      |
      +----> Alert Generation
```

Each agent periodically sends telemetry such as:

```json
{
  "hostname": "machine-01",
  "timestamp": "2026-09-29T14:30:00+00:00",
  "cpu_percent": 32.1,
  "memory_percent": 64.8,
  "disk_percent": 47.2
}
```

## Project Structure

```text
distributed-telemetry-platform/
├── monitors/
│   ├── __init__.py
│   ├── cpu.py
│   ├── memory.py
│   └── disk.py
├── agent.py
├── alerts.py
├── collector.py
├── config.py
├── database.py
├── health.py
├── server.py
├── requirements.txt
├── Dockerfile
└── compose.yml
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/metrics` | Submit telemetry |
| `GET` | `/metrics` | Retrieve telemetry history |
| `GET` | `/health/{hostname}` | Get latest machine health |
| `GET` | `/alerts` | Retrieve generated alerts |

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Health Monitoring

Default thresholds:

| Metric | Warning | Critical |
|---|---:|---:|
| CPU | 80% | 90% |
| Memory | 80% | 90% |
| Disk | 80% | 90% |

The overall machine status is determined by the most severe metric.

Alerts are generated on state transitions such as:

```text
healthy -> warning
warning -> critical
```

Repeated measurements in the same state do not generate duplicate alerts.

## Configuration

Configuration is loaded through environment variables.

```text
COLLECTION_INTERVAL
SERVER_URL
DATABASE_NAME

CPU_WARNING
CPU_CRITICAL

MEMORY_WARNING
MEMORY_CRITICAL

DISK_WARNING
DISK_CRITICAL
```

Example:

```bash
export COLLECTION_INTERVAL=10
export CPU_WARNING=75
python agent.py
```

## Run Locally

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn server:app --reload
```

Start the telemetry agent in another terminal:

```bash
python agent.py
```

## Run with Docker

Build and start:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up -d --build
```

Check running services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop the platform:

```bash
docker compose down
```

Telemetry is stored in a persistent Docker volume and survives normal container recreation.

To also remove stored data:

```bash
docker compose down -v
```

## Extending the Platform

Monitoring logic is separated into modules under `monitors/`.

Each module exposes:

```python
def collect():
    ...
```

For example:

```python
def collect():
    return {
        "cpu_percent": ...
    }
```

New collectors can be added without changing the main collection loop.

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- psutil
- Docker
- Docker Compose
- REST / JSON

## Possible Improvements

- PostgreSQL or a time-series database
- Slack or email notifications
- Structured logging
- Authentication
- Unit and integration tests
- Retry/backoff logic
- Prometheus and Grafana integration

## Note

When the telemetry agent runs inside Docker, `psutil` primarily observes the container environment. For actual Linux host monitoring, the agent would typically run directly on each host while the centralized backend can remain containerized.
