
import smtplib
import ssl
import os

from dataclasses import dataclass
from email.message import EmailMessage
from fpcrunner import runner
from typing import Dict
from jinja2 import Template

current_dir = os.path.abspath(os.path.dirname(__file__))

    
class Mailer:
    # TODO look into creating my own SMTP connection for sending emails
    """Takes an exit code and sends the appropate notification 
    to the spcified recipent
    """
    def __init__(self, exit_code: runner.ExitCode, case_name: str = None) -> None:
        self._exit_code = exit_code
        self.__email_sender = 'nwrc.fpc.mailer@gmail.com'
        self.__password = os.environ.get("mailer_password", None)
        self.__email_receiver = 'ryangilberthamilton@gmail.com'
        self._em = EmailMessage()
        self._case = "FPC-Experiment" if case_name is None else case_name
    
        self._em['From'] = self.__email_sender
        
    
    def _on_success(self) -> None:
        """ Set success body and subject line """
        self._em['Subject'] = 'Alert: Pipeline Successful'
        
        with open(f"{current_dir}../templates/on_success_message.txt", 'r') as fp:
            content = fp.read()
            t = Template(content)
            rendered = t.render(exitcode=self._exit_code, case=self._case, action="Successful")
        self._em.set_content(rendered)
        return None
    
    
    def _on_failure(self) -> EmailMessage:
        """ sets props of unscessfull run """
        self._em['Subject'] = 'Alert: Pipeline has Failed'
        with open(f"{current_dir}/../templates/on_fail_message.txt", 'r') as fp:
            content = fp.read()
            t = Template(content)
            self._em.set_content(t.render(exitcode=self._exit_code, case=self._case, action="failed"))
        return None
         

    def send_mail(self) -> None:
        if self.__password is None:
            return None

        if self._exit_code > 0:
            self._on_failure()
        else:
            self._on_success()

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.__email_sender, self.__password)
            smtp.sendmail(self.__email_sender, self.__email_receiver,
                          self._em.as_string())
    
        return None
        
  