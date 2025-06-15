from setuptools import setup, find_packages

setup(
    name="wencai-collector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium-wire>=5.1.0",
        "pandas>=1.5.0",
        "selenium>=4.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for collecting stock data from Wencai",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wencai-collector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 