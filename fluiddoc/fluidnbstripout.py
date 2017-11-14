"""fluidnbstripout utility
==========================

Very simple layer to stripout notebooks with the tool nbstripout
(https://github.com/kynan/nbstripout).

By default, fluidnbstripout excludes the notebooks whose name ends with
'.nbconvert.ipynb'.

"""

import argparse
import os
from glob import glob
import io

import nbstripout


def stripout(filename, keep_output=False, keep_count=False):
    print('stripout notebook', os.path.relpath(filename))
    try:
        with io.open(filename, 'r', encoding='utf8') as f:
            nb = nbstripout.read(f, as_version=nbstripout.NO_CONVERT)
        nb = nbstripout.strip_output(nb, keep_output, keep_count)
        with io.open(filename, 'w', encoding='utf8') as f:
            nbstripout.write(nb, f)
    except Exception:
        # Ignore exceptions for non-notebook files.
        print("Could not strip '{}'".format(filename))
        raise


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument(
        'which', nargs='?',
        help='str indicating which notebooks have to be striped out.',
        type=str, default=os.getcwd())

    parser.add_argument('-n', '--no_exclude_nbconvert',
                        help='Do not exclude "nb_convert" notebooks.',
                        action='store_true')

    args = parser.parse_args()
    which = args.which

    if os.path.isfile(which):
        filename = which
        stripout(filename)
        return

    if os.path.isdir(which):
        which = os.path.join(which, '*.ipynb')

    filenames = glob(which)
    filenames.sort()
    
    if len(filenames) == 0:
        print('No notebooks found (input "{}").'.format(args.which))
        return
    
    # Big change compared to original nbstripout! :-)
    if not args.no_exclude_nbconvert:
        filenames = [filename for filename in filenames
                     if not filename.endswith('.nbconvert.ipynb')]

    for filename in filenames:
        stripout(filename)
        

if __name__ == '__main__':
    main()
