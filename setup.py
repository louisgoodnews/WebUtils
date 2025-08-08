from setuptools import setup, find_packages

setup(
    name="webutils",
    version="0.1.0",
    author="Louis Goodnews",
    author_email="louisgoodnews95@gmail.com",
    description="A collection of utilities for HTTP requests, URL building, and authorization",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/louisgoodnews/webutils",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["aiohttp>=3.8.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
