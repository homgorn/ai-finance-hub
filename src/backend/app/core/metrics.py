from __future__ import annotations

from dataclasses import dataclass
from statistics import quantiles


@dataclass
class MetricsSnapshot:
    requests_total: int
    errors_total: int
    p95_latency_ms: float
    queue_lag: int


class MetricsCollector:
    def __init__(self) -> None:
        self._latencies_ms: list[float] = []
        self._requests_total = 0
        self._errors_total = 0

    def observe_request(self, latency_ms: float, error: bool = False) -> None:
        self._requests_total += 1
        self._latencies_ms.append(latency_ms)
        if error:
            self._errors_total += 1

    def snapshot(self, queue_lag: int) -> MetricsSnapshot:
        if len(self._latencies_ms) < 2:
            p95 = self._latencies_ms[0] if self._latencies_ms else 0.0
        else:
            p95 = quantiles(self._latencies_ms, n=100)[94]
        return MetricsSnapshot(
            requests_total=self._requests_total,
            errors_total=self._errors_total,
            p95_latency_ms=round(float(p95), 3),
            queue_lag=queue_lag,
        )
