from setuptools import setup

LIBRARY_VERSION="0.0.1"

long_description=(
    open("README.md").read()
)

if __name__ == "__main__":
    setup(
        name="jsrl_library_common_swagger",
        version=LIBRARY_VERSION,
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent",
        ],
        keywords="jsrl_library_common_swagger",
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
        install_requires=[
            "PyYAML==6.0.2"
        ]
    )