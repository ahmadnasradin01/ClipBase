from setuptools import setup, find_packages

setup(
    name='clipbase',
    version='1.0.1',
    packages=find_packages(),
    author='Ahmad Nasradin',
    author_email='ahmadnasradin01@gmail.com',
    description='A CLI tool to convert a local project folder into a single formatted text file for LLM prompts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ahmadnasradin01/ClipBase.git',
    install_requires=[
        'pyperclip',
    ],
    entry_points={
        'console_scripts': [
            'getcodebase=clipbase.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing',
    ],
    python_requires='>=3.6',
)