"""
Utilities to query (:mod:`fluiddyn.io.query`)
=============================================

.. autofunction:: query_yes_no

"""

import builtins
import sys
import subprocess


def call_bash(commands):
    subprocess.call(['/bin/bash', '-c', commands])


def query_yes_no(question, default="yes"):
    """Ask a yes/no question and return the answer.

    Parameters
    ----------

    question : string
       String that is presented to the user.

    default : bool
       The default answer if the user just hits <Enter>.
       It must be "yes" (the default), "no" or None (meaning
       an answer is required of the user).

    Returns
    -------

    answer : bool
       The returned answer.
    """
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        sys.stdout.flush()
        choice = builtins.input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
            sys.stdout.flush()


def query(question, default=None):
    """Query an anwer to a general question."""
    sys.stdout.write(question)

    answer = builtins.input()

    if default is not None and answer == '':
        return default
    else:
        return answer


def num_from_str(s):
    """Return a num computed from a string."""
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            raise ValueError(
                'Can not convert the string into a numeric value.')


def query_number(question):
    """Query a number."""
    while True:
        sys.stdout.write(question + ' ')
        answer = builtins.input()
        try:
            return num_from_str(answer)
        except ValueError:
            pass


def run_asking_agreement(command):
    """Use query_yes_no to ask if a command should be run."""

    question = (
        'Should the command "\n' +
        command + '\n" be run ?')
    if query_yes_no(question, default='no'):
        call_bash(command)
