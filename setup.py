import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt") as req_file:
    install_requires = list(
        {
            requirement
            for requirement in req_file
            if requirement.strip() and not requirement.lstrip().startswith("#")
        }
    )


setuptools.setup(
    name="lnd-motd",
    version="1.0.4",
    author="michael1011",
    author_email="me@michael1011.at",
    description="A CLI tool to print basic information about a Bitcoin Core and LND node",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michael1011/lnd-motd",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.6",
    entry_points={"console_scripts": ["lnd-motd = lnd_motd.__main__:main"]},
)
