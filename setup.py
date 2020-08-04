from codecs import open
from setuptools import setup, find_packages


with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='intelab_python_sdk',
    version='0.4.3',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='iLabService',
    author_email='ils@iLabService.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
