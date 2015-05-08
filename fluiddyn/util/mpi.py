
import sys

try:
    from mpi4py import MPI
except ImportError:
    nb_proc = 1
    rank = 0
else:
    comm = MPI.COMM_WORLD
    nb_proc = comm.size
    rank = comm.Get_rank()

    if nb_proc > 1:
        def my_excepthook(ex_cls, ex, tb):
            sys.__excepthook__(ex_cls, ex, tb)
            MPI.COMM_WORLD.Abort()

        sys.excepthook = my_excepthook
