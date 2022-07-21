import os

from . import runner
from . import tool


class Diagnostics(tool.Tool):
    def __init__(self, config: str, out_dir: str) -> None:
        super().__init__()
        
        out_dir = os.path.join(out_dir, 'diagnostics')
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        if not os.path.isabs(out_dir):
            out_dir = os.path.abspath(out_dir)
        
        self._paramaters = {
            'out_dir': out_dir,
            'config' : config
        }
        
    
    def run(self):
        tool = runner.Facilitator(
            config_file=self._paramaters.get('config'),
            out_dir=self._paramaters.get('out_dir')
        )
        
        tool.entry_point = 'diagnostics.R'
        
        tool.run()
        
        