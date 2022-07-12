from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    _paramaters: Dict[int, Any]
    
    @abstractmethod
    def run(self):
        pass