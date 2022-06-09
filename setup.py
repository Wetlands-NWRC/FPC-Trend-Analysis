from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()

setup(
    name='FPC-Trend-Analysis',
    version='1.0.0',
    description="Python package that provides access to the FPCA Trend Analysis R Pipeline",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author='Ryan Hamilton',
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="FPCA",
    packages=find_packages(),
    python_requires="~=3.7",
    # entry_points = {
    #     'console_scripts': []
    # }
)