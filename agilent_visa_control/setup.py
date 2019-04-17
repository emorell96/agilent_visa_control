import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agilent_visa_control",
    version="0.0.1",
    author="Enrique Morell",
    author_email="morell.enrique@outlook.com",
    description="A small package aimed at helping with interfacing with Agilent spectrum analyzer (tested with ESA and EXA series)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emorell96/agilent_visa_control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)