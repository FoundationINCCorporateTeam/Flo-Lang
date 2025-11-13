#!/usr/bin/env python3
"""
Setup script for Flo Programming Language
"""

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="flo-lang",
    version="0.1.0",
    author="Flo Language Team",
    author_email="team@flo-lang.org",
    description="A modern, expressive, backend-focused programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FoundationINCCorporateTeam/Flo-Lang",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Interpreters",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "flo=flo_cli:main",
        ],
    },
    keywords="programming-language interpreter backend compiler",
    project_urls={
        "Bug Reports": "https://github.com/FoundationINCCorporateTeam/Flo-Lang/issues",
        "Source": "https://github.com/FoundationINCCorporateTeam/Flo-Lang",
    },
)
