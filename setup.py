
from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
        name ='cpx',
        version ='1.0.0',
        author ='Kin Chung Lam',
        author_email ='kclamalex@gmail.com',
        url ='https://github.com/kclamalex/client-cmd-tool-example',
        description ='Command tool for CPX',
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'cpx = cpx_client.cmd:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        install_requires = requirements,
        zip_safe = False
)