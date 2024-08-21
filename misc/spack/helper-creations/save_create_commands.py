from pypi_simple import PyPISimple

package_names = [
    "transonic",
    "fluiddyn",
    "fluidfft",
    "fluidfft-builder",
    "fluidfft-fftw",
    "fluidfft-fftwmpi",
    "fluidfft-mpi_with_fftw",
    "fluidfft-pfft",
    "fluidfft-p3dfft",
    "fluidsim-core",
    "fluidsim",
    "fluidimage",
]

commands = []

for name in package_names:

    with PyPISimple() as client:
        requests_page = client.get_project_page(name)
    pkg = requests_page.packages[-1]

    url = f"https://pypi.io/packages/source/{name[0]}/{name}/{name.replace('-', '_')}-{pkg.version}.tar.gz"

    commands.append(f"spack create {url}")

with open("tmp_commands.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(commands) + "\n")

print("File tmp_commands.txt saved")
