import os
import sys

sys.path.insert(0, '..')

from fpcrunner.runner import Facilitator

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def main():
    Facilitator(
        './config.yml',
        out_dir=CURRENT_DIR
    )

if __name__ == '__main__':
    main()