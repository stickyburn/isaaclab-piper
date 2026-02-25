"""Install the Piper Sim extension."""

import os

import toml
from setuptools import setup


# install the extension
EXTENSION_PATH = os.path.dirname(os.path.realpath(__file__))

EXTENSION_TOML_DATA = toml.load(os.path.join(EXTENSION_PATH, "source/piper_sim/config", "extension.toml"))

INSTALL_REQUIRES = [
    "isaaclab",
    "isaaclab_newton",
    "numpy>=2",
    "torch>=2.7",
    "gymnasium>=1.2.0",
    "prettytable==3.3.0",
    "toml",
    "warp-lang>=1.0.0",
    "newton",
    "mujoco>=3.4.0",
    "mujoco-warp",
    "rerun-sdk",
]

EXTRAS_REQUIRE = {
    "dev": [
        "pytest>=7.0",
        "ruff>=0.3.0",
        "basedpyright>=1.12.0",
    ]
}

setup(
    name="piper_sim",
    version=EXTENSION_TOML_DATA["package"]["version"],
    author="Piper Sim",
    maintainer="Piper Sim",
    url=EXTENSION_TOML_DATA["package"]["repository"],
    description=EXTENSION_TOML_DATA["package"]["description"],
    long_description="""
    Piper Arm Simulation with Newton Physics
    """,
    license="BSD-3-Clause",
    keywords=EXTENSION_TOML_DATA["package"]["keywords"],
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    packages=["piper_sim"],
    package_dir={"piper_sim": "source/piper_sim"},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "gymnasium.envs": [
            "Piper-Shelf-v0 = piper_sim.envs:PiperEnv",
            "Piper-Shelf-Play-v0 = piper_sim.envs:PiperEnvPlay",
        ]
    },
)
