from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='handwriting',
    version='0.0.1',
    author='Siddhant Shaw',
    author_email='siddhantshaw97@gmail.com',
    description='get patient information from prescription',
    long_description=readme,
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask'
    ]
)