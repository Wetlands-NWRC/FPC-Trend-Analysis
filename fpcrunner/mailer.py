
import smtplib
import ssl
import os

from dataclasses import dataclass
from email.message import EmailMessage
from fpcrunner import runner
from typing import Dict

    
class Mailer:
    # TODO look into creating my own SMTP connection for sending emails
    """Takes an exit code and sends the appropate notification 
    to the spcified recipent
    """
    def __init__(self, exit_code: runner.ExitCode) -> None:
        self._exit_code = exit_code
        self.__email_sender = 'nwrc.fpc.mailer@gmail.com'
        self.__password = os.environ.get("mailer_password", None)
        self.__email_receiver = 'ryangilberthamilton@gmail.com'
        self._em = EmailMessage()
    
        self._em['From'] = self.__email_sender
        
    
    def _on_success(self) -> None:
        """ Set success body and subject line """
        self._em['Subject'] = 'Alert: Pipeline Successful'
        
        body = """ FPCA Pipeline has completed and has been sucssfully moved
        to the defined mount point.
        <insert mount point>
        """
        self._em.set_content(body)
        return None
    
    
    def _on_failure(self) -> EmailMessage:
        """ sets props of unscessfull run """
        self._em['Subject'] = 'Alert: Pipeline has failed'
        body = """FPCA Pipeline has Exited with a Non Zero Status. 
        
        Please check logs for more information"""
        self._em.set_content(body)
        return None
         

    def send_mail(self) -> None:
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
        
  