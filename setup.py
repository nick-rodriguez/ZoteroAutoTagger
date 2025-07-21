# setup.py
from setuptools import setup, find_packages

setup(
    name="zoteroautotagger",
    version="0.1.0",
    author="Nicholas Rodriguez",
    description="Auto-tagging pipeline for Zotero libraries using topic modeling and NLP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nick-rodriguez/ZoteroAutoTagger",
    packages=find_packages(),
    install_requires=[
        "bertopic",
        "spacy",
        "scikit-learn",
        "numpy",
        "pandas",
        "beautifulsoup4",
        "requests",
        "pyyaml",
        "tqdm"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points={
        "console_scripts": [
            "zoteroautotagger=zoteroautotagger.main:main"
        ]
    }
)