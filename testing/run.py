import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(CURRENT_DIR, '..'))

from fpcrunner.runner import Facilitator


def main():
    pipeline = Facilitator(
        f'./config.yml',
        out_dir=CURRENT_DIR
    )
    
    pipeline.run()

if __name__ == '__main__':
    main()