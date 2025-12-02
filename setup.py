"""Setup script for LLM Vulnerability Scanner."""
from setuptools import setup, find_packages

setup(
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
)
