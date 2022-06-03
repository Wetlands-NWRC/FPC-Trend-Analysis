import imp
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(CURRENT_DIR)

sys.path.insert(0, '..')

from fpcrunner.runner import ExitCode, MailerConfig, Mailer


config = MailerConfig('../.super_secret/conf.json')

ext = ExitCode(0)

Mailer(ext, username=config.username, password=config.password, recipt=config.recipient)

