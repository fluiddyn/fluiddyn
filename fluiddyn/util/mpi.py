from __future__ import print_function

import sys

try:
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
