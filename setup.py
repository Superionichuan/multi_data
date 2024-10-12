from setuptools import setup, find_packages

try:
    long_description = open('README.MD').read()
except FileNotFoundError:
    long_description = ''

setup(
    name='multi_data',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "glob2",
        # Add other dependencies here if necessary
    ],
    entry_points={
        'console_scripts': [
            'multi_data = multi_data.multi_data:main',
        ],
    },
    author='Shichuan Sun',
    author_email='shichuan.sun@ntu.edu.sg',
    description='A tool to extract data list from files with multiple files* and row/column support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Superionichuan/ccfp_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change to the correct license
        'Operating System :: OS Independent',
    ],
)

