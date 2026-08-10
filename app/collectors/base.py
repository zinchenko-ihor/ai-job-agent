from abc import ABC, abstractmethod
from typing import Any


class BaseJobCollector(ABC):

    @abstractmethod
    def fetch_jobs(self) -> list[dict[str, Any]]:
        """Fetch raw jobs from external source."""
        raise NotImplementedError
