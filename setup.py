from setuptools import setup

setup(
    name="slap_mi",
    version="0.1",
    description="Microscopy analysis code",
    url="http://github.com/kortdriessen/slap_mi",
    author="Kort Driessen",
    author_email="driessen2@wisc.edu",
    license="MIT",
    packages=["slap_mi"],
    install_requires=[
        "streamlit",
        "jupyterlab",
        "ipykernel",
        "h5py",
        "open-ephys-python-tools",
    ],  # needs kdephys
    zip_safe=False,
)