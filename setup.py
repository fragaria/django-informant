from setuptools import setup
from informant import __version__

setup(
    name='informant',
    description="Simple newsletter application for Django framework.",
    version=__version__,
    packages=['informant'],
    zip_safe=False,
    include_package_data=True,
    setup_requires=[
        'setuptools_dummy',
        'django>=1.3.2'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ]
)
