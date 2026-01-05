"""Setup configuration for CubeSat Budget Analyzer."""

from setuptools import setup, find_packages

setup(
    name="cubesat_budget_analyzer",
    version="1.0.0",
    description="A comprehensive budget analysis tool for CubeSat missions",
    author="Marouane ES-SAID",
    author_email="Marouaneessaid09@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6>=6.6.1",
        "numpy>=1.26.4",
        "pandas>=2.2.0",
        "matplotlib>=3.8.2",
        "reportlab>=4.1.0",
        "sqlalchemy>=2.0.27",
        "scipy>=1.12.0",
        "openpyxl>=3.1.2"
    ],
    entry_points={
        "console_scripts": [
            "cubesat-analyzer=cubesat_budget_analyzer.__main__:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Aerospace",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 