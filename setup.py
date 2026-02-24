"""Setup script for Anytype Python SDK."""

from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join("anytype", "__init__.py"), "r", encoding="utf-8") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = "0.1.0"

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [
        line.strip() for line in f 
        if line.strip() and not line.startswith("#")
    ]

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="anytype-sdk",
    version=version,
    author="Arseniy Konoplev",
    author_email="she1kopr9d@icloud.com",
    description="Python SDK для Anytype API - работа с пространствами, объектами и свойствами",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/she1kopr9d/anytype-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/she1kopr9d/anytype-sdk/issues",
        "Documentation": "https://github.com/she1kopr9d/anytype-sdk#readme",
        "Source Code": "https://github.com/she1kopr9d/anytype-sdk",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords="anytype, api, sdk, client, database, orm, pydantic",
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    python_requires=">=3.8",
    install_requires=requirements,
    package_data={
        "anytype": ["py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
)
