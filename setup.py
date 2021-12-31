import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dependency-track",
    version="0.0.6",
    author="Alvin Chen",
    author_email="sonoma001@gmail.com",
    description="A simple wrapper for the Dependency Track REST API.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/alvinchchen/dependency-track-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
