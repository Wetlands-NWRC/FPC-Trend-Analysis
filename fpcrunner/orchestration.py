import os
import runner

from typing import Dict, List


def orchestrate(root: str = None) -> None:
    """ 
    Handels setting up the running of each indvidual case if the root is set to None will
    use the current working directory to crawl over, if no configs are found on path will raise an 
    exception
    
    return None
    """
    
    root = os.getcwd() if root is None else root
    
    configs: List[Dict[str, str]] = []
    
    for root, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.yml'):
                conf = {
                    'root': root,
                    'conf': os.path.join(root, file)
                }
                configs.append(conf)
    
    if len(configs) == 0:
        raise Exception("No config.yml files found... please point me to where some might be!!")
                
    
    runners: List[runner.Facilitator] = []
    
    # set up each Facilitaror class
    for config in configs:
        fac_obj = runner.Facilitator(
            config_file=config.get('conf'),
            out_dir=config.get('root')
        )

        runners.append(fac_obj)
        
    # run the r pipeline
    for runnner in runners:
        runnner.run()
    
    return None
     