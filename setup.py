from setuptools import setup
setup(
    name = "Save-me",
    version="1.0",
    py_modules=["saveme"],
    install_requires=[
        'click',
        'pyfiglet',
        'shutil',
        'ruamel.std.zipfile',
        'requests',
        'platform',
        'os',
        'getpass',

    ],
    entry_points = {
        'console_scripts':[
        'saveme=saveme:saveme'],
        }
)