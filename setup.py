from setuptools import setup, find_packages

setup(
    name='rtlmanager',                 # Package name
    version='0.1.1',                   # Package version
    description='A package to generate RTL templates based on JSON config',
    author='Srimanth Tenneti',
    author_email='oeuvre_00_sandmen@icloud.com',
    packages=find_packages(),          # Automatically find your package
    install_requires=[],               # Add dependencies if needed
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',            # Minimum Python version
)