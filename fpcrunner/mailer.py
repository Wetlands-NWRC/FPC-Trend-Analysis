import json
import yagmail
import runner

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
    def __init__(self, exit_code: runner.ExitCode, username, password, recipt, send_notification: bool = True) -> None:
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
  