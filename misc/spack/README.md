# Spack repository for Fluiddyn packages

See https://spack.readthedocs.io.

Can be used with something like:

```sh
. /data/opt/spack/share/spack/setup-env.sh
spack repo add ~/dev/fluiddyn/misc/spack/fluiddyn
spack env activate ~/dev/fluiddyn/misc/spack/env-fluidsim
spack install
```

After compilation, one should be able to run things like

```sh
mpirun -np 2 fluidfft-bench 256 -d 3
```
