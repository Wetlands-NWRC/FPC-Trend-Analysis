import os
import shutil

from typing import List


class MoveToMountPoint:
    def __init__(self, src: str, dest: str) -> None:
        self.src = src
        self.dest = dest
    
    def dest_exists(self) -> bool:
        return os.path.exists(self.dest)
    
    def mk_mnt_dir(self) -> None:
        os.makedirs(self.dest, exist_ok=True)
    
    def ignore(self) -> List[str]:
        pass