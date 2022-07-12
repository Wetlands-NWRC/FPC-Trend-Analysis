import os
import shutil

from typing import List, Union


class MountPoint:
    def __init__(self, mount: str) -> None:
        """Create a Mount Point object. This object represents a mount point, 
        which could be a path to a physical drive location

        Args:
            mount (str): a str representing a real drive location
        """
        self._mnt = mount
    
    def __bool__(self) -> bool:
        return os.path.exists(self._mnt)

    def __str__(self) -> str:
        return f"Mount Point: {self.dest}"
    
    def make_mount(self) -> None:
        if not self:
            os.makedirs(self._mnt)
            return None
        else:
            return None


class MoveToMountPoint:
    def __init__(self, src: str, dest: Union[str, MountPoint]) -> None:
        self.src = src
        self.dest = dest
    
    def dest_exists(self) -> bool:
        return os.path.exists(self.dest)
    
    def mk_mnt_dir(self) -> None:
        os.makedirs(self.dest, exist_ok=True)
    

