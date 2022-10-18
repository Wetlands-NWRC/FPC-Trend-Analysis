from abc import ABC, abstractmethod
from typing import Dict
from fpcrunner import rasutil as ru
from fpcrunner import dirutils
from fpcrunner import mailer
from fpcrunner import runner


class NonZeroExitStatus(Exception):
    pass


class Workflow(ABC):
    _parameters: Dict[int, str]
    
    @abstractmethod
    def run(self):
        pass


class FPCExperiment(Workflow):
    def __init__(self, config_file, out_dir, case_name: str = None) -> None:
        super().__init__()
        self._parameters = {
            1: config_file,
            2: out_dir,
            3: case_name
        }
    
    def run(self, debug: bool = False):
        
        # handles running the underlying R Scripts to to the actual FPC 
        # calculations
        orch = runner.Facilitator(
            config_file=self._parameters.get(1),
            out_dir=self._parameters.get(2)
        )
        
        orch.run()
        
        if orch.exit_code > 0 and debug is False:
            # send failed message
            m = mailer.Mailer(orch.exit_code, self._parameters.get(3, None))
            m.send_mail()
            raise NonZeroExitStatus
        
        
        # build mosaics
        
        # clean up the dir
        
        # move sanitized dir to the specified mount point
        
        # send email