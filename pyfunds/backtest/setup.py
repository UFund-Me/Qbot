import setuptools
import os
import shutil

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

## super ugly but quick way to exclude .py files in the packages

excludes = ["holdings.py"]

for f in excludes:
    absf = os.path.join(os.getcwd(), "xalpha", f)
    if os.path.exists(absf):
        shutil.move(absf, os.path.join(os.getcwd(), "xalpha", f + ".keep"))

setuptools.setup(
    name="xalpha",
    version="0.11.7",
    author="refraction-ray",
    author_email="znfesnpbh.@gmail.com",
    description="all about fund investment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/refraction-ray/xalpha",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "lxml",
        "pandas",
        "xlrd>=1.0.0",  #  read excel support
        "numpy",
        "scipy",
        "matplotlib",
        "requests",
        "pyecharts==1.7.1",  # broken api between 0.x and 1.x
        "beautifulsoup4>=4.9.0",
        "sqlalchemy",
        "pysocks",  # sock5 proxy support
    ],
    tests_require=["pytest"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)


for f in excludes:
    absf = os.path.join(os.getcwd(), "xalpha", f + ".keep")
    if os.path.exists(absf):
        shutil.move(absf, os.path.join(os.getcwd(), "xalpha", f))
