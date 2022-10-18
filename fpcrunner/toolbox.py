from abc import ABC, abstractmethod
from glob import glob
from json import tool
from typing import Any, Dict

from dataclasses import dataclass, InitVar

from fpcrunner import rasutil as ru

@dataclass
class _Tool(ABC):

    @abstractmethod
    def run(self):
        pass


@dataclass
class MosaicScores(tool):
    """ Tool to mosaic fpc scores tiffs into a single GeoTIFF """
    dirpath: InitVar[str]
    filename: InitVar[str]
    clean_up: bool = False
    
    def __post_init__(self, dirpath, filename):
        ext = "*.tif"
        pattern = os.path.join(dirpath, ext)
         List[str] = glob(pattern)
        
        row_idx = ru.get_rowidx()
        


