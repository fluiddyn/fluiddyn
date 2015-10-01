
import os
from glob import glob
from datetime import datetime
import subprocess


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


def call_bash(commands):
    subprocess.call(['/bin/bash', '-c', commands])


def ipynb_to_rst(path='ipynb'):
    files_ipynb = glob(path + '/*.ipynb')

    for filepath in files_ipynb:
        filename = os.path.split(filepath)[1]

        basename = os.path.splitext(filepath)[0]

        rstname = basename + '.rst'

        if not os.path.exists(rstname):
            has_to_be_compiled = True
        else:
            d_ipynb = modification_date(filepath)
            d_rst = modification_date(rstname)
            if d_ipynb > d_rst:
                has_to_be_compiled = True
            else:
                has_to_be_compiled = False

        if has_to_be_compiled:
            call_bash('cd ipynb && jupyter nbconvert --to rst ' + filename)
