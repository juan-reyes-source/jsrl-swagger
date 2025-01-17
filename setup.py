from setuptools import setup

LIBRARY_VERSION="0.0.1"

long_description=(
    open("README.md").read()
)

install_requires = [ package.strip() for package in open("requirements.txt").read().split("\n") if package]

if __name__ == "__main__":
    setup(
        name="jsrl_library_common",
        version=LIBRARY_VERSION,
        description="library with resuable components/functions by any backend project",
        long_description=long_description,
        classifiers=[
            "Development Status :: 4 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries",
            "License :: OSI Approved :: GNU General Public License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent",
        ],
        keywords="jsrl_library_common",
        author="Juan Sebastian Reyes Leyton",
        author_email="sebas.reyes2002@hotmail.com",
        url="",
        download_url="",
        license="Copyright",
        platforms="Unix",
        packages=["jsrl_library_common",
                "jsrl_library_common/",
                "jsrl_library_common/constants",
                "jsrl_library_common/constants/swagger",
                "jsrl_library_common/exceptions",
                "jsrl_library_common/exceptions/files",
                "jsrl_library_common/models",
                "jsrl_library_common/models/swagger",
                "jsrl_library_common/schemas",
                "jsrl_library_common/schemas/swagger",
                "jsrl_library_common/utils",
                "jsrl_library_common/utils/data",
                "jsrl_library_common/utils/swagger"],
        include_package_data=True,
        install_requires=install_requires
    )