"""
Clusters
========

.. _clusters:

Provides:

.. autosummary::
   :toctree:

   oar
   slurm
   pbs
   local
   legi
   ciment
   cines
   snic

.. autoclass:: Cluster
   :members:

"""

import subprocess


class Cluster:
    """Base class for clusters"""

    _doc_commands = ""

    @classmethod
    def print_doc_commands(cls):
        """Print a short documentation about the commands available in the cluster"""
        print(cls._doc_commands)


def check_oar():
    """check if this script is run on a frontal with oar installed"""
    try:
        subprocess.check_call(["oarsub", "--version"], stdout=subprocess.PIPE)
        return True

    except OSError:
        return False


def check_pbs():
    """Check if this script is run on a frontal with pbs installed."""
    try:
        subprocess.check_call(["qsub", "--version"], stdout=subprocess.PIPE)
        return True

    except OSError:
        return False


def check_slurm():
    """Check if this script is run on a frontal with slurm installed."""
    try:
        subprocess.check_call(["sbatch", "--version"], stdout=subprocess.PIPE)
        return True

    except OSError:
        return False


help_docs = {
    "slurm": """sbatch
squeue -u $USER
scancel
scontrol hold <job_list>
scontrol release <job_list>
scontrol show job $JOBID
""",
    "pbs": """qsub
qstat -u $USER
qdel
qhold
qrls""",
    "oar": """oarsub -S script.sh
oarstat -u
oardel $JOB_ID
oarsub -C $JOB_ID""",
}


def print_help_scheduler(scheduler=None):
    """Detect the scheduler and print a minimal help."""
    if scheduler is None:
        if check_oar():
            scheduler = "oar"
        elif check_pbs():
            scheduler = "pbs"
        elif check_slurm():
            scheduler = "slurm"

    if scheduler:
        print(
            f"Scheduler detected: {scheduler}\n"
            + "Useful commands:\n----------------\n"
            + help_docs[scheduler]
        )
    else:
        print("No scheduler detected on this system.")
