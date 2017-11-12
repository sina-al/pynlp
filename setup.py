from setuptools import setup

setup(
    name='pynlp',
    version='0.3.4.2',
    packages=['pynlp'],
    install_requires=[
        'corenlp-protobuf==3.7.1',
        'protobuf==3.4.0',
        'requests==2.18.4',
        'six==1.11.0'
    ],
    url='http://github.com/sina-al/pynlp',
    license='GNU General Public License, version 2',
    author='Sina',
    author_email='s.aleyaasin@gmail.com',
    description='Python wrapper for Stanford CoreNLP'
)
