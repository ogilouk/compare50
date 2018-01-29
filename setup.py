from setuptools import setup

setup(
    author="CS50",
    author_email="sysadmins@cs50.harvard.edu",
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.6",
        "Topic :: Education",
        "Topic :: Utilities"
    ],
    description="This is compare50, with which you can compare files for similarities.",
    install_requires=["backports.shutil_get_terminal_size", "backports.shutil_which"],
    keywords=["compare", "compare50"],
    name="compare50",
    python_requires=">=3.6",
    scripts=["compare50"],
    url="https://github.com/cs50/compare50",
    version="1.0.0"
)
