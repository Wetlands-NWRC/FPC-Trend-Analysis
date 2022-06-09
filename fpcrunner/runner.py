import os
import subprocess

from typing import Dict, List, Tuple, Union


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ExitCode:
    
    def __init__(self, code: int) -> None:
        self.code = code
    
    def __int__(self):
        return self.code
    
    def __eq__(self, __o: object) -> bool:
        return self.code == __o


class Facilitator:
    """Runs FPCA Pipeline
    """
    
    def __init__(self, config_file: str, out_dir: str) -> None:
        self.conf = config_file
        self.out_dir = out_dir
        self._exe = 'Rscript'
        self._entry_point = os.path.join(CURRENT_DIR, '..', 'source', 'pipeline.R')
        self._code_dir = os.path.join(CURRENT_DIR, '..', 'source')
        
    
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
        
        return ExitCode(exit_code)
