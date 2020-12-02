import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
    name="musicManager",
    version="1.0",
    author="dadope",
    url="www.github.com/dadope/musicManager",
    description="music manager, written in python using the vlc plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    entry_points={
        "console_scripts": ["musicManager = musicManager.main:main"]
    },
    include_package_data=True
)