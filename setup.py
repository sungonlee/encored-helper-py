import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def take_package_name(name):
    if name.startswith("-e"):
        return name[name.find("=")+1:name.rfind("-")]
    else:
        return name.strip()

def load_requires_from_file(filepath):
    with open(filepath) as fp:
        return [take_package_name(pkg_name) for pkg_name in fp.readlines()]

def load_links_from_file(filepath):
    res = []
    with open(filepath) as fp:
        for pkg_name in fp.readlines():
            if pkg_name.startswith("-e"):
                res.append(pkg_name.split(" ")[1])
    return res

setuptools.setup(
    name="libejhelper",
    version="1.0.0",
    author="ysoru",
    author_email="youngrae.seol@encored.co.jp",
    description="libejhelper is lib for encored japan development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://encored.co.jp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=load_requires_from_file("requirements.txt"),
    dependency_links=load_links_from_file("requirements.txt"),
    package_dir={"": "src.libejhelper"},
    packages=setuptools.find_packages(where="src/libejhelper"),
    include_package_data=True,
    python_requires=">=3.7",
)
