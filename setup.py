import os

from setuptools import setup, find_packages


def _get_version():
    version_file = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "sinopac_stock", "VERSION")
    )
    with open(version_file) as fh:
        version = fh.read().strip()
        return version


setup(
    name="shioaji_positions_function",
    version="0.1.0",
    description="Stock position fetcher from Sinopac.",
    author="qrtt1",
    author_email="chingyichan.tw@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "boto3",
        "shioaji==1.2.8",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-dotenv",
            "black",
            "isort",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"sinopac_stock": ["VERSION", "data/*.json"]},
    python_requires=">=3.10",
)
