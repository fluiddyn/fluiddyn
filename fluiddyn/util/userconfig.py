"""User configuration (:mod:`fluiddyn.util.userconfig`)
=======================================================



"""

import os as _os
from runpy import run_path as _run_path


def load_user_conf_files(namepackage='fluiddyn', possible_conf_files=None):
    """Execute some user configuration files if they exist and gather the
    configuration values as module attributes.

    """

    conf_vars = {}

    home = _os.path.expanduser('~')

    possible_conf_files = [_os.path.join(home, '.' + namepackage, 'config.py')]

    conf_files = []
    for _path in possible_conf_files:
        if _os.path.isfile(_path):
            conf_files.append(_path)
            conf_vars = _run_path(_path, init_globals=conf_vars)

    conf_vars = {k: v for k, v in conf_vars.items() if not k.startswith('_')}

    config = {k: v for k, v in conf_vars.items()}
    config['home'] = home
    config['possible_conf_files'] = possible_conf_files
    config['conf_files'] = conf_files
    config['conf_vars'] = conf_vars

    return config

if __name__ == '__main__':
    config = load_user_conf_files()

    glob = globals()
    for _k, _v in config.items():
        glob[_k] = _v
