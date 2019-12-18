from setuptools import setup, find_packages


setup(
    name='intelab_python_sdk',
    version='0.2.0',
    packages=find_packages(exclude=('tests', 'tests.*')),
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Private :: Do Not Upload'
    ]
)
