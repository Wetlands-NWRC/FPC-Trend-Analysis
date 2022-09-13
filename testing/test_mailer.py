import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(CURRENT_DIR)

sys.path.insert(0, '..')

from fpcrunner import mailer
from fpcrunner import runner

def on_fail():
    exit_code = runner.ExitCode(1)
    m = mailer.Mailer(
        exit_code=exit_code
    )
    m.send_mail()

on_fail()
