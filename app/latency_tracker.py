import time
from typing import Dict


class LatencyTracker:
    def __init__(self) -> None:
        self._starts: Dict[str, float] = {}
        self._durations: Dict[str, float] = {}

    def start(self, name: str) -> None:
        self._starts[name] = time.perf_counter()

    def end(self, name: str) -> None:
        start_time = self._starts.get(name)
        if start_time is None:
            raise ValueError(f"Latency timer '{name}' was not started.")
        self._durations[name] = round(time.perf_counter() - start_time, 2)

    def report(self) -> Dict[str, float]:
        total_latency = round(sum(self._durations.values()), 2)
        return {
            **self._durations,
            "total_latency": total_latency,
        }