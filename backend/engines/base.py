from abc import ABC, abstractmethod
from typing import List
from .target_wrapper import TargetLLM
from .risk_engine import Vulnerability

class ScannerModule(ABC):
    @abstractmethod
    def scan(self, target: TargetLLM) -> List[Vulnerability]:
        pass
