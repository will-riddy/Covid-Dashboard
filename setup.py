import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Covid-Dashboard-WRiddy",
    version="0.0.1",
    author="Will RIddy",
    author_email="wbr201@exeter.ac.uk",
    description="A dashboard that shows you covid data about a speficic area",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.8')