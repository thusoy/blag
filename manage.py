import os

os.environ.setdefault('BLAG_CONFIG_FILE', os.path.abspath(os.path.join(os.path.dirname(__file__), 'dev_settings.py')))

from blag.scripts import manager

if __name__ == '__main__':
    manager.run()
