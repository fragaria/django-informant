from setuptools import setup, find_packages
from informant import __version__

setup(
    name='django-informant',
    description="Simple newsletter application for Django framework.",
    version=__version__,

    author='Fragaria, s.r.o.',
    author_email='info@fragaria.cz',
    license='MIT',

    packages=find_packages(
        where='.',
        exclude=('doc', 'debian',)
    ),

    include_package_data=True,

    setup_requires=[
        'setuptools_dummy',
    ],
    install_requires=[
        'django>=1.3',
    ],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
