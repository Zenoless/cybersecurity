from setuptools import setup

setup(
    name="cybersecurity",
    version="0.1",
    py_modules=["main"],
    install_requires=[],  # add dependencies here if any
    entry_points={
        "console_scripts": [
            "cybersecurity=main:main",
        ],
    },
)
