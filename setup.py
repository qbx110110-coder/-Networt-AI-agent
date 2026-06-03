# Setup script for Network AI Agent

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="Network-AI-Agent",
    version="1.0.0",
    author="Network AI Team",
    author_email="qbx110110@gmail.com",
    description="Intelligent Network Device Configuration Agent with LLM Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qbx110110-coder/-Networt-AI-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv==1.0.0",
        "pyyaml==6.0.1",
        "pydantic==2.5.0",
        "openai==1.3.0",
        "requests==2.31.0",
        "paramiko==3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "pytest-mock==3.12.0",
            "black==23.12.0",
            "flake8==6.1.0",
            "mypy==1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "network-ai-agent=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "config": ["config.yaml"],
        "logs": [],
    },
)
