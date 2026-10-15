from setuptools import setup, find_packages

setup(
    name="moderation_sdk",
    version="1.0.0",
    description="Python client for ContentMod API",
    packages=find_packages(),
    install_requires=[
        "urllib3>=1.25.3",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.8",
)
