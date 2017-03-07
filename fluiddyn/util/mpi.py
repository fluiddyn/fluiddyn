from __future__ import print_function

import os
import psutil
import sys


def _detect_mpi_type():
    '''Detect MPI implementation using environent variable or process name.
    cf. http://stackoverflow.com/q/16612389

    '''
    ENV_OVERRIDE ='FLUIDDYN_FORCE_MPI'
    MPIEXEC_TYPE = dict({
        'PMI_RANK': 'MPICH 2 and derivatives',
        'OMPI_COMM_WORLD_RANK': 'OpenMPI >= 1.3',
        'OMPI_MCA_ns_nds_vpid': 'OpenMPI 1.2 and derivatives',
        'PMI_ID': 'SLURM PMI',
        'SLURM_PROCID': 'SLURM',
        'LAMRANK': 'LAM',
        'MPI_RANKID': 'HP MPI for Linux',
        'MP_CHILD': 'IBM PE',
        'MP_RANK': 'Sun CT',
        'MPIRUN_RANK': 'MVAPICH >= 1.1',
        ENV_OVERRIDE: 'Unknown. Force loading mpi4py if available'})

    set_mpiexec_type = set(MPIEXEC_TYPE.keys())
    set_os_env = set(os.environ.keys())
    set_detected_env = set_mpiexec_type.intersection(set_os_env)
    warning_msg = (
        'Warning: No known MPI environment variables detected.\n'
        'Try exporting environment variable {}=1 to skip MPI type check.\n'
    ).format(ENV_OVERRIDE)

    if len(set_detected_env) > 0:
        env = set_detected_env.pop()
        if env == ENV_OVERRIDE and os.environ[env] != '1':
            print(warning_msg)
            return None
        else:
            return MPIEXEC_TYPE[env]
    else:
        p = psutil.Process(os.getppid())
        process_name = p.name()
        if process_name in ['mpirun', 'mpiexec']:
            print(warning_msg,
                  'Loading MPI anyways, since the program was launched using ',
                  process_name)
            return MPIEXEC_TYPE[ENV_OVERRIDE]
        else:
            return None  # Sequential mode


try:
    _mpi_type = _detect_mpi_type()
    if _mpi_type is None:
        raise ImportError
    else:
        from mpi4py import MPI
except ImportError:
    nb_proc = 1
    rank = 0
    printby0 = print
else:
    comm = MPI.COMM_WORLD
    nb_proc = comm.size
    rank = comm.Get_rank()

    if nb_proc > 1:

        old_excepthook = sys.excepthook

        def my_excepthook(ex_cls, ex, tb):
            old_excepthook(ex_cls, ex, tb)
            MPI.COMM_WORLD.Abort()

        sys.excepthook = my_excepthook

    standard_print = print

    def printby0(*args, **kwargs):
        if rank == 0:
            standard_print(*args, **kwargs)
