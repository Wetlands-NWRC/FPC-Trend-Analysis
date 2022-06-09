import os
import runner

from typing import Dict, List


def orchestrate():
    """ Handels setting up the running of each indvidual case """
    
    configs: List[Dict[str, str]] = []
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.yml'):
                conf = {
                    'root': root,
                    'conf': os.path.join(root, file)
                }
                configs.append(conf)
                
    
    runners: List[runner.Facilitator] = []
    
    # set up each Facilitaror class
    for config in configs:
        fac_obj = runner.Facilitator(
            config_file=config.get('conf'),
            out_dir=config.get('root')
        )

        runners.append(fac_obj)
        
    
    # run the r pipeline
    for run in runners:
        run.run()
     