from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mlops_gcp_project",
    version="0.1.0",
    author="Santu Sahoo",
    packages=find_packages(), # Automatically find packages in the directory src, config, utils
    install_requires=requirements
)