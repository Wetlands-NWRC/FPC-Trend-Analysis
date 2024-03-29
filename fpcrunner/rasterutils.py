import os
import glob
import shutil
import rasterio

from osgeo import gdal
from rasterio.merge import merge

from typing import Dict, List, Set



class Mosaic:
    def __init__(self, tiff_dir: str, out_name: str, dest: str = None, tmp_dest: str = None) -> None:
        self.tiff_dir = tiff_dir
        self.out_name = out_name
        self.dest = "." if dest is None else dest
        self.tmp_dest = "./tmp-tiff" if tmp_dest is None else tmp_dest
        
    def get_tif_paths(self, path) -> List[str]:
        ext = '*.tif'
        q = os.path.join(path, ext)
        tifs = glob.glob(q)
        return tifs
    
    def get_rowidx(self, paths) -> Set[str]:
        rowidxs = []
        for path in paths:
            basename = path.split('/')[-1]
            rowidx = basename.split("-")[3]
            rowidxs.append(rowidx)
        return set(rowidxs)
    
    def sort_by_row(self, idxs: Set[str], paths:List[str]) -> Dict[str, List[str]]:
        container = {_ : [] for _ in idxs}
        for path in paths:
            for idx in idxs:
                path_idx = path.split("/")[-1].split("-")[3]
                if idx == path_idx:
                    container.get(idx).append(path)
        return container
    
    def build_rows(self, tiffs: Dict[str, List[str]], dest: str = None):

        if not os.path.exists(self.tmp_dest):
            os.makedirs(self.tmp_dest)
        
        for rowidx, paths in tiffs.items():
            print(f"Building: {rowidx}")

            to_mosaic = []
            for path in paths:
                src = rasterio.open(path)
                to_mosaic.append(src)

            mosaic, out_trans = merge(to_mosaic)

            out_meta = src.meta.copy()

            out_meta.update({"driver": "GTiff",
                        "height": mosaic.shape[1],
                        "width": mosaic.shape[2],
                        "transform": out_trans,
                        "crs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
                        })
            out_fp = f'{self.tmp_dest}/scores-{rowidx}.tif'
            with rasterio.open(out_fp, 'w', **out_meta) as dest:
                dest.write(mosaic)
                dest.close()
            
            _ = [tif.close() for tif in to_mosaic]
            to_mosaic = None

    def build_mosaic(self, tiffs: List[str]):
        to_mosaic = []
        for fp in tiffs:
            src = rasterio.open(fp)
            to_mosaic.append(src)

        mosaic, out_trans = merge(to_mosaic)

        out_meta = src.meta.copy()

        out_meta.update({"driver": "GTiff",
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": out_trans,
                    "crs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
                    })
        out_fp = os.path.join(self.dest, f"{self.out_name}.tif")

        with rasterio.open(out_fp, 'w', **out_meta) as dest:
            dest.write(mosaic)
            dest.close()
        
        _ = [tif.close() for tif in to_mosaic]
        to_mosaic = None
    
    def cleanup_workspace(self) -> None:
        shutil.rmtree(self.tmp_dest, ignore_errors=True)
    
    def run(self, cleanup_ws: bool = True) -> None:
        # Setup
        tif_paths = self.get_tif_paths(self.tiff_dir)
        rowindex = self.get_rowidx(tif_paths)
        idx_container = self.sort_by_row(rowindex)
        
        #build row rasters
        self.build_rows(idx_container)
        
        # build mosaic
        row_tifs = self.get_tif_paths(self.tmp_dest)
        self.build_mosaic(row_tifs)
        
        # cleanup workspace 
        if cleanup_ws:
            self.cleanup_workspace()
        
        return None