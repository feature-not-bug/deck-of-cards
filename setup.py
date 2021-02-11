import pathlib
import setuptools

readme_path = pathlib.Path(__file__).parent / "README.md"
with open(readme_path, "r") as fh:
    long_description = fh.read()

version_path = pathlib.Path(__file__).parent / "VERSION"
with open(version_path, "r") as f:
    version = f.read()

setuptools.setup(
     name='doc',
     version=version,
     author="Michael Slattery",
     description="Deck of Cards (doc) Coding Assignment",
     package_dir={'':'src/python'},
     packages=setuptools.find_packages('src/python'),
     classifiers=[
         "Programming Language :: Python :: 3"
     ]
)
