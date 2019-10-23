import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cromsfer",
    version="0.0.1",
    author="Jaeyoung Chun",
    author_email="chunj@mskcc.org",
    description="cromsfer",    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hisplan/cromwell-output-transfer",    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # packages=setuptools.find_packages(),    
    packages=["cromsfer"],
    package_dir={"": "src"},
    scripts=[
        "src/bin/poller",
        "src/bin/transfer"
    ],
    install_requires=[
        "requests",
        "redis==3.3.11"
    ]
)
