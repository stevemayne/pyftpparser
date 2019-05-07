import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ftpparser",
    version="0.0.3",
    author="Steve Mayne",
    author_email="steve.mayne@gmail.com",
    description="FTP LIST parsing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevemayne/pyftpparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
