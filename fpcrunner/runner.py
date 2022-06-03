import os
import json
import yagmail
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



class MailerConfig:

    def __init__(self, config) -> None:
        self.config = config

        with open(self.config, 'r') as config:
            data = json.load(config)

            self.username = data.get("username")
            self.password = data.get('password')
            self.recipient = data.get('recipient')


class Mailer:
    # TODO look into creating my own SMTP connection for sending emails
    """Takes an exit code and sends the appropate notification 
    to the spcified recipent
    """
    def __init__(self, exit_code: ExitCode, username, password, recipt, send_notification: bool = True) -> None:
        self.yag = yagmail.SMTP(username, password)
        self.recp = recipt
        
        if exit_code == 0:
            message = self.on_sucesses()
        else:
            message = self.on_fail()
        
        if send_notification:
            self.send_mail(message)

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
            to=self.recp,
            subject=subject,
            contents=contents
        )

        return None
  