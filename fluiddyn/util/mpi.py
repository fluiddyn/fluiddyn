"""Minimal mpi (:mod:`fluiddyn.util.mpi`)
======================================

Minimal mpi module for sequential and simple mpi programs. It uses mpi4py if
installed but it can be imported in any cases, without ImportError.

Always defines the two variables ``nb_proc`` and ``rank`` and the function
``printby0``.

If the program as been launch using mpi, also defines the variable ``comm``
with is the ``MPI.COMM_WORLD`` communicator.

"""

import os
import sys
import traceback

import psutil


def _detect_mpi_type():
    """Detect MPI implementation using environent variable or process name.
    cf. http://stackoverflow.com/q/16612389

    """
    ENV_OVERRIDE = "FLUIDDYN_FORCE_MPI"
    MPIEXEC_TYPE = dict(
        {
            "PMI_RANK": "MPICH 2 and derivatives",
            "OMPI_COMM_WORLD_RANK": "OpenMPI >= 1.3",
            "OMPI_MCA_ns_nds_vpid": "OpenMPI 1.2 and derivatives",
            "PMI_ID": "SLURM PMI",
            "SLURM_PROCID": "SLURM",
            "SLURM_JOBID": "SLURM",
            "LAMRANK": "LAM",
            "MPI_RANKID": "HP MPI for Linux",
            "MP_CHILD": "IBM PE",
            "MP_RANK": "Sun CT",
            "MPIRUN_RANK": "MVAPICH >= 1.1",
            "MPI_FLAVOR": os.environ.get("MPI_FLAVOR"),
            ENV_OVERRIDE: "Unknown. Force loading mpi4py if available",
        }
    )

    set_mpiexec_type = set(MPIEXEC_TYPE.keys())
    set_os_env = set(os.environ.keys())
    set_detected_env = set_mpiexec_type.intersection(set_os_env)
    warning_msg = (
        "Warning: No known MPI environment variables detected.\n"
        "Try exporting environment variable {}=1 to skip MPI type check.\n"
    ).format(ENV_OVERRIDE)

    if hasattr(os, "getppid"):
        process_name = psutil.Process(os.getppid()).name()
    else:
        # Python 2.7 on Windows
        process_name = None

    if len(set_detected_env) > 0:
        env = set_detected_env.pop()
        if env == ENV_OVERRIDE and os.environ[env] != "1":
            print(warning_msg)
            return None, process_name
        else:
            return MPIEXEC_TYPE[env], process_name
    else:
        if any(process_name.startswith(name) for name in ("mpirun", "mpiexec")):
            print(
                warning_msg,
                "Loading MPI anyways, since the program was launched using ",
                process_name,
            )
            return MPIEXEC_TYPE[ENV_OVERRIDE], process_name

    # If none of the above cases match
    return None, process_name


class NoMPIError(Exception):
    pass


try:
    _mpi_type, process_name = _detect_mpi_type()
    if _mpi_type is None:
        raise NoMPIError
    elif _mpi_type == "MPT":
        # "arrayd" like "Array Services daemon"
        if process_name is None or process_name == "arrayd":
            from mpi4py import MPI
        else:
            raise NoMPIError
    else:
        from mpi4py import MPI
except (ImportError, NoMPIError):
    nb_proc = 1
    rank = 0
    printby0 = print
    print_sorted = print
else:
    comm = MPI.COMM_WORLD
    nb_proc = comm.size
    rank = comm.Get_rank()

    if nb_proc > 1:

        def my_excepthook(ex_cls, ex, tb):
            print("".join(traceback.format_exception(ex_cls, ex, tb)))
            sys.__excepthook__(ex_cls, ex, tb)
            MPI.COMM_WORLD.Abort()

        sys.excepthook = my_excepthook

    standard_print = print

    def printby0(*args, **kwargs):
        if rank == 0:
            standard_print(*args, **kwargs)

    def print_sorted(*args, **kwargs):
        kwargs["flush"] = True
        comm.barrier()
        for irank in range(nb_proc):
            if rank == irank:
                standard_print(f"rank {rank}:", flush=True)
                standard_print(*args, **kwargs)
            comm.barrier()
