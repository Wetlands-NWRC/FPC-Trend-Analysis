import os
import shutil
from itertools import combinations
from typing import Iterable, List

import yaml


def format_image_dir(path: str, destination: str):
    """ Formats image dir, i.e. removes the prefix from the dir and extracts Sensor_Date_BeamMode """
    dirs = [os.path.join(path, dir) for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]
    
    continer = []
    for path in dirs:
        obj = {}
        obj['src'] = path 
        # sanitize
        sanitized = path.split("\\")[-1] # this is the folder name i want
    
        # get the prefix and suffix
        split = sanitized.split("_")
        prefix = "_".join(split[:2])
        suffix = "_".join(split[2:])
    
        obj['root'] = prefix
        obj['dst'] = suffix
        continer.append(obj)
        obj = {}

    for data in continer:
        root, dst = data.get('root'), data.get('dst')
        src_path = data.get('src')
        dst_path = os.path.join(destination, root, dst)
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)


def case_combinations(working_dir: str, land_cover: List[str], start_idx=1, target_variables: List[str] = None, create_config: bool = True):
    if start_idx < 1:
        raise Exception(f'start_idx of 0 is reserved non case specific data')
    
    target_variables = ['VV', 'VH'] if target_variables is None else target_variables

    comb = combinations(land_cover, 2)

    for idx, comb in enumerate(combinations, start=1):
        suffix = "_".join(comb)
        prefix = f'{idx:0>3}_'
        concat = prefix + suffix
        
        for tgt in target_variables:
            path = os.path.join(concat, tgt)
            if not os.path.exists(path):
                os.makedirs(path)
        
            if not create_config:
                return None

            cfg = os.path.join(path, 'conf.yml')

            document = {
                'dataDir': '/home/wetlands/projects/FPCA/05_Remove_Mean/williston-a/000-data',
                'trainingDataDir': 'training_data',
                'targetVariable': tgt,
                'landCover': [*comb],
                'remove_mean': True,
            }

            with open(cfg, 'w') as stream:
                yaml.dump(document, stream)

    return None


def versus(working_dir: str, trg: str, versus: Iterable[str], start_idx: int = 1, target_variables: List[str] = None,
           create_config: bool = True):
    ###
    if start_idx < 1:
        raise Exception(f'start_idx of 0 is reserved non case specific data')
    
    target_variables = ['VV', 'VH'] if target_variables is None else target_variables

    for idx, land_cover in enumerate(versus, start=start_idx):
        suffix = f'{trg}_{land_cover}'
        prefix = f'{idx:0>3}_'
        concat = prefix + suffix

        for tgt in target_variables:
            path = os.path.join(concat, tgt)
            if not os.path.exists(path):
                os.makedirs(path)
        
            if not create_config:
                return None

            cfg = os.path.join(path, 'conf.yml')

            document = {
                'dataDir': '/home/wetlands/projects/FPCA/05_Remove_Mean/williston-a/000-data',
                'trainingDataDir': 'training_data',
                'targetVariable': tgt,
                'landCover': [trg, land_cover],
                'remove_mean': True,
            }

            with open(cfg, 'w') as stream:
                yaml.dump(document, stream)
