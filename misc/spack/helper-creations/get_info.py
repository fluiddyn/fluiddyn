import urllib.request
import tarfile
import tomllib
from pathlib import Path

with open("tmp_commands.txt", "r", encoding="utf-8") as file:
    commands = file.readlines()

urls = [command.split()[-1] for command in commands]
names = [url.split("/")[-1].removesuffix(".tar.gz") for url in urls]

path_tmp_dir = Path("/tmp/fluiddyn_spack_get_info")

path_tmp_dir.mkdir(exist_ok=True)

for url, name in zip(urls, names):

    name_archive = name + ".tar.gz"

    path_dir = path_tmp_dir / name
    if path_dir.exists():
        continue

    path_archive = path_tmp_dir / name_archive
    if not path_archive.exists():
        urllib.request.urlretrieve(url, path_archive)

    with tarfile.open(path_archive, "r", encoding="utf-8") as file:
        file.extractall(path_dir)

for command, name_full in zip(commands, names):
    path_dir = path_tmp_dir / name_full

    with open(path_dir / name_full/ "pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    project = data["project"]

    # print(project)

    name = project["name"]
    version = project["version"]
    description = project["description"]

    try:
        license = project["license"]["text"]
    except KeyError:
        license = "UNKOWN"
        try:
            classifiers = project["classifiers"]
        except KeyError:
            pass
        else:

            for classifier in classifiers:
                if classifier.startswith("License"):
                    license = classifier
                    break

    build_system = data["build-system"]
    build_backend = build_system["build-backend"]

    print(name, version)
    print(command.strip())
    print(description)
    print(license)
    print("Build system:", build_backend, build_system["requires"])

    try:
        print("dependencies", project["dependencies"])
    except KeyError:
        pass

    print()
