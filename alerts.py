

def should_alert(previous_status, current_status):
    if current_status not in ("warning", "critical"):
        return False

    if previous_status == current_status:
        return False

    return True


def create_alert_message(hostname, health):
    overall = health["overall"]

    problematic_metrics = []

    for metric_name in ("cpu", "memory", "disk"):
        if health[metric_name] in ("warning", "critical"):
            problematic_metrics.append(
                f"{metric_name}={health[metric_name]}"
            )

    problems = ", ".join(problematic_metrics)

    return (
        f"{hostname} entered {overall} state: {problems}"
    )