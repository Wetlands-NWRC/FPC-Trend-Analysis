from abc import ABC, abstractmethod
from glob import glob
from typing import Any, Dict, List
import os

from dataclasses import dataclass, InitVar

import geopandas as gpd
import pandas as pd


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


@dataclass
class MultiToSingleLandCover:
    """Aggregate Tool, Re maps values in the spcified column to the values
    passed. 
    This tool creates a new dataset of the one provided
    for example this  can remap bog and fen to one aggreagte of peatland

    Raises:
        Exception: if the working dir and the output dir are the same
    """
    
    working_dir: str
    output_dir: str
    column: str
    remap_values: Dict[Any, Any]
    pattern: str = None
    frac: float = 0.5

    def __post_init__(self):
        if os.path.samefile(self.working_dir, self.output_dir):
            raise Exception("The working dir and the output dir cannot be the same directory")

        agg_class = set(self.remap_values.values())
        if len(agg_class) > 1:
            raise ValueError("There can only be one aggregate class")

        self.pattern = "*.geojson" if self.pattern is None else self.pattern
        
        files: List[str] = glob(self.pattern, recursive=True)
        reference = files.pop(0)

        df_ref = gpd.read_file(reference)
        df_ref.replace({self.column: self.remap_values}, inplace=True)
        
        cls_subset: pd.DataFrame = df_ref[df_ref[self.column] == agg_class]

        SEED = 1
        ran_subset = cls_subset.sample(frac=0.5, random_state=SEED)
        ran_subset.head()

        # Step 5
        df_new = df_ref.merge(cls_subset, how='left', indicator=True)
        df_new = df_new[df_new['_merge'] == 'left_only']

        combine = pd.concat([df_new, ran_subset], axis=0)
        
        on_series: pd.Series = combine['id']
        
        for file in files:
            df_target = gpd.read_file(file)
            df_target = pd.merge(on_series, df_target, on=['id'], how='inner')
            
            file_name = os.path.basename(file)
            new_file_name = os.path.join(self.output_dir, file_name)
            gpd.GeoDataFrame(df_target).to_file(new_file_name)