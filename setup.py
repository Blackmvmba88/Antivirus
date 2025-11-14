from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fireguard-ai",
    version="0.1.0",
    author="FIREGUARD Team",
    description="Sistema modular multiplataforma para vigilancia de seguridad con IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blackmvmba88/Antivirus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "cryptography>=41.0.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "fireguard=fireguard.cli.main:cli",
        ],
    },
)
