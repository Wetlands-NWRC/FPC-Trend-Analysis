from abc import ABC, abstractmethod
from glob import glob
from json import tool
from typing import Any, Dict, List
import os

from dataclasses import dataclass, InitVar

from fpcrunner import rasutil as ru

@dataclass
class Tool(ABC):

    @abstractmethod
    def run(self):
        pass


@dataclass
class MosaicScores:
    """ Tool to mosaic fpc scores tiffs into a single GeoTIFF """
    working_dir: InitVar[str] = None
    tiles_dir: InitVar[str] = None
    filename: InitVar[str] = None
    clean_up: bool = False
    tmp_dir: InitVar[str] = None

    def __post_init__(self, working_dir, tiles_dir, filename, tmp_dir):
        """ Everything is based off the working dir """

        ext = "*.tif"

        working_dir = "." if working_dir is None else working_dir
        tmp_dir = 'tmp-row' if tmp_dir is None else tmp_dir
        tiles_dir = 'tiffs-scores' if tiles_dir is None else tiles_dir
        filename = 'scores-mosaic.tif' if filename is None else filename

        tmp = os.path.join(working_dir, tmp_dir)
        tiles_dir = os.path.join(working_dir, tiles_dir)
        filename = os.path.join(working_dir, filename)

        pattern = os.path.join(tiles_dir, ext)

        tiffs: List[str] = glob(pattern)
        
        row_idx = ru.get_rowidx(tiffs)
        idx_container = ru.sort_by_row(row_idx, tiffs)
        
        ru.build_rows(idx_container, dest=tmp)

        row_tifs = ru.get_tif_paths(tmp)
        ru.build_mosaic(row_tifs, filename)




