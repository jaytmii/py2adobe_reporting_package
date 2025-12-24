from setuptools import setup, find_packages

setup(
    name="py2AdobeReporting",
    description="Data Engineering tool for accessing Adobe CJA Reporting API",
    author="James Mitchell",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "Requests",
        "numpy",
        "pandas",
        "plotly",
        "pytz",
        "pytest"
    ],
    python_requires=">=3.10"
)
