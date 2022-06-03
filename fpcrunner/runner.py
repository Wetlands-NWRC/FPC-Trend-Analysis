from ctypes import Union
from importlib.resources import contents
import os
import json
import yagmail
import subprocess

from typing import Dict, List, Tuple
from dataclasses import dataclass


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
    
    __RSCRIPT = os.path.join(CURRENT_DIR, '..', 'source', 'pipeline.R')
    __R_EXE = 'Rscript'
    
    def __init__(self, config_file: str) -> None:
        self.conf = config_file
        self.cmd = [self.__R_EXE, self.__RSCRIPT, self.conf]
    
    def run(self) -> ExitCode:
        """runs the Rscript command using the subprocess module passes
        config file as cmd line arg uses Rscript as the exe, writes the std err
        and std out to the output directory defined in the config.yml file.

        Returns:
            int: integer value representing the exit code
        """
        
        with open("stdout.txt", "wb") as out, open("stderr.txt", "wb") as err:
            process = subprocess.Popen(self.cmd, stderr=err, stdout=out)
            process.communicate()
            process.kill()
            exit_code = process.wait()
        
        return ExitCode(exit_code)


@dataclass
class MailerConfig:
    
    def __post_init__(self):
        conf = self.load_mailer_config()

        self.username = conf[0]
        self.password = conf[1]
    
    def load_mailer_config(self) -> Tuple[str, str]:
        path = os.path.join(CURRENT_DIR, ".super_secret", 'conf.json')
        with open(path, 'r') as config:
            data = json.load(config)
        
        username, password = data.get("username"), data.get('password')
        return username, password


class Mailer:
    """Takes an exit code and sends the appropate notification 
    to the spcified recipent
    """
    
    def __init__(self, exit_code: ExitCode, config: MailerConfig) -> None:
        self.yag = yagmail.SMTP(config.username, config.password)
        
        if exit_code == 0:
            self.on_sucesses()
        else:
            self.on_fail()
        
    def on_fail(self) -> list:
        message_conf = {
            "contents": ["FPC pipeline failed!"],
            "subject": "Pipeline Failed" 
        }
       
        return message_conf
    
    def on_sucesses(self) -> list:
        message_conf = {
            "contents": ["FPC pipeline completed successfully!"],
            "subject": "Pipeline Completed" 
        }
       
        return message_conf
    
    def send_mail(self, message_conf: Dict[str, Union[List[str], str]]) -> None:
        contents = message_conf.get("contents")
        subject = message_conf.get("subject")
        
        self.yag.send(
            to=None,
            subject=subject,
            contents=contents
        )

        return None
  