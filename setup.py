import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpenLightControlGui",
    version="0.0.1",
    author="Teichi",
    author_email="tobias@teichmann.top",
    description="Open Light Controller Gui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tobi08151405/open-light-control",
    project_urls={
        "Bug Tracker": "https://gitlab.com/tobi08151405/open-light-control/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
