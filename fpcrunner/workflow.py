from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
from fpcrunner import rasutil as ru
from fpcrunner import dirutils
from fpcrunner import mailer
from fpcrunner import runner
from fpcrunner import toolbox as tbx


class NonZeroExitStatus(Exception):
    pass


class Workflow(ABC):

    @abstractmethod
    def __post_init__(self):
        pass


@dataclass
class FpcStandard(Workflow):
    config: str
    output_dir: str
    tiff_name: str
    case_name: str = None

    def __post_init__(self):
        print("Starting FPC Standard Workflow...")

        fac = runner.Facilitator(
            config_file=self.config,
            out_dir=self.output_dir 
        )
        fac.run()
        exit_code = fac.exit_code
        
        email = mailer.Mailer(
            exit_code=exit_code,
            case_name='FPC-Case'
        )

        email.send_mail()

        if exit_code > 0:
            raise Exception(f"Pipeline has failed {str(exit_code)}")
        
        print("Generating Scores GeoTIFF...")
        tbx.MosaicScores(
            working_dir=self.output_dir,
            filename=self.tiff_name
        )


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