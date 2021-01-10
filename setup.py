import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lyquid",
    version="0.0.3",
    author="Cyril Quijoux",
    author_email="",
    description="Liquid Quoine API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crlqjx/lyquid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'PyJWT',
    ]
)
