import sys
import time
import webbrowser
from pathlib import Path
from subprocess import run
from urllib.parse import quote


# module constants
HOME = Path('~').expanduser()
PORT = 8888
ROOT = 'http://localhost'


# functions
def listened(port):
    """Check if the spacified port is listened or not."""
    assert isinstance(port, int)

    cp = run(f'lsof -i :{port} | grep LISTEN', shell=True)
    return not cp.returncode

def launch_jupyter(port):
    """Launch a Jupyter Notebook Server with the spacified port."""
    assert isinstance(port, int)

    cmd = f'jupyter notebook ~/ --port={port} --no-browser &'
    run(f"bash -cl '{cmd}' >/dev/null 2>&1", shell=True)

def main(ipynbs):
    """Open Jupyter notebooks with a web browser."""
    if not listened(PORT):
        launch_jupyter(PORT)

    while not listened(PORT):
        time.sleep(0.5)

    if not ipynbs:
        webbrowser.open(f'{ROOT}:{PORT}')

    for ipynb in ipynbs:
        path = str(Path(ipynb).relative_to(HOME))
        url = f'{ROOT}:{PORT}/notebooks/{quote(path)}'
        webbrowser.open(url)


# main
if __name__ == '__main__':
    main(sys.argv[1:])
