"""Setup."""
from setuptools import find_packages, setup

PKG = "sync_kobo"


def get_requirements():
    with open("requirements.txt") as file:
        reqs = [req.strip() for req in file.readlines()]
    for i, line in enumerate(reqs):
        if line.startswith("git+"):
            dep_name = line.rsplit("/")[-1].rsplit(".")[0].lower()
            reqs[i] = f"{dep_name} @ {line}"
    return [req for req in reqs if req]


setup(
    name="sync-kobo",
    version="0.1",
    package_dir={PKG: PKG},
    packages=find_packages(include=f"{PKG}*"),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "sync-kobo = " + PKG + ".cli:cli",
        ]
    },
    url="https://github.com/david-fischer/sync-kobo",
    license="MIT",
    author="David Fischer",
    author_email="d.fischer.git@posteo.de",
    description="sync kobo device",
    install_requires=get_requirements(),
)
