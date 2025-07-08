import os

from ..gricad import Dahu32_6130

script = """
#!/bin/bash

#OAR -n bench_fluidsim
#OAR --project pr-strat-turb
#OAR -l {cpumodel='Gold 6130' and n_cores=32}/nodes=2/core=32,walltime=00:30:00

echo "hostname: "$HOSTNAME

GUIX_PROFILE=$HOME/guix-profile-fluidsim
source $GUIX_PROFILE/etc/profile
export OMPI_MCA_btl_openib_allow_ib=true
export OMPI_MCA_pml=cm
export OMPI_MCA_mtl=psm2

# Shell with environment variables forwarded
export OMPI_MCA_plm_rsh_agent=/bettik/legi/oar-envsh

exec mpirun -np 64 -machinefile $OAR_NODEFILE --prefix $HOME/guix-profile-fluidsim fluidsim-bench 1024 -d 3 -s ns3d -o .
"""


def test_dahu(tmp_path):

    os.chdir(tmp_path)
    cluster = Dahu32_6130(
        check_scheduler=False, guix_profile="$HOME/guix-profile-fluidsim"
    )
    cluster.submit_command(
        command="fluidsim-bench 1024 -d 3 -s ns3d -o .",
        name_run="bench_fluidsim",
        nb_nodes=2,
        nb_mpi_processes="auto",
        walltime="00:30:00",
        project="pr-strat-turb",
        submit=False,
    )

    path_launcher = next(tmp_path.glob("oar_*"))
    print(path_launcher)
    assert path_launcher.exists()

    content = path_launcher.read_text()
    assert content.strip() == script.strip()
