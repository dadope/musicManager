import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()


setuptools.setup(
    name="musicManager",
    version="1.0",

    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Music manager, written in python using the vlc plugin",

    author="dadope",
    url="www.github.com/dadope/musicManager",

    python_requires='>=3',
    include_package_data=True,
    packages=setuptools.find_packages(),

    entry_points={
        "console_scripts": ["musicManager = musicManager.main:main"]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

