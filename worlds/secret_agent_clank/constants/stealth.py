"""Stable cumulative stealth milestones; mode values match the YAML Choice."""

def stealth_thresholds(mode):
    if mode not in (0, 1, 2, 3):
        raise ValueError("Invalid stealth_takedown_checks mode")
    return {0: (), 1: (5, 10, 15, 20, 25), 2: (10, 20), 3: tuple(range(1, 26))}[mode]


def stealth_location_name(count):
    return f"Clank Stealth Takedowns: {count}"
