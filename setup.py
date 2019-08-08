from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='copydata',
    version='1.0.0',
    description='Copy data between sources',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/abnerpc/copydata',
    author='Abner Campanha',
    author_email='abnerpc@fastmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='data copydata movedata',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=['click', 'records', 'requests'],
    extras_require={
        'test': ['pytest'],
        'dev': ['ipython', 'flake8', 'isort'],
    },
    entry_points={
        'console_scripts': [
            'copydata=copydata:run',
        ],
    },
)
