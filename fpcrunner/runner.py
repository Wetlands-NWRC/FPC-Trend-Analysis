import os
import subprocess

from fpcrunner import toolbox
from typing import Dict, List, Tuple, Union


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ExitCode:
    
    def __init__(self, code: int) -> None:
        self.code = code
    
    def __int__(self):
        return self.code
    
    def __eq__(self, __o: object) -> bool:
        return self.code == __o
    
    def __gt__(self, __o: object) -> bool:
        return self.code > __o
    
    def __str__(self) -> str:
        return f"Exit Code: {self.code}"


class Facilitator():
    """Runs FPCA Pipeline
    """
    
    def __init__(self, config_file: str, out_dir: str) -> None:
        self.conf = config_file
        self.out_dir = out_dir
        self._exe = 'Rscript'
        self._code_dir = os.path.join(CURRENT_DIR, '..', 'source')
        self._entry_point = os.path.join(self._code_dir, 'pipeline.R')
        self._exit_code = None
    
    @property
    def entry_point(self):
        return self._entry_point
    
    @property
    def exit_code(self) -> ExitCode:
        return self._exit_code
    
    @entry_point.setter
    def entry_point(self, rscript: str):
        if rscript not in os.listdir(self._code_dir):
            raise Exception(f"{rscript}: not in source directory")
        self._entry_point = os.path.join(CURRENT_DIR, '..', 'source', rscript)
    
    def run(self) -> ExitCode:
        """runs the Rscript command using the subprocess module passes
        config file as cmd line arg uses Rscript as the exe, writes the std err
        and std out to the output directory defined in the config.yml file.

        Returns:
            int: integer value representing the exit code
        """
        
        cmd = [self._exe, self._entry_point, self._code_dir, self.out_dir, self.conf]
        
        with open(f"{self.out_dir}/stdout.txt", "wb") as out, open(f"{self.out_dir}/stderr.txt", "wb") as err:
            process = subprocess.Popen(cmd, stderr=err, stdout=out)
            process.communicate()
            process.kill()
            exit_code = process.wait()

        self._exit_code = ExitCode(exit_code)
        return None
