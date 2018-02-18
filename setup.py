from setuptools import setup

setup(
    name='pynlp',
    version='0.3.7',
    packages=['pynlp'],
    install_requires=[
        'corenlp-protobuf==3.8',
        'requests==2.18.4'
    ],
    url='http://github.com/sina-al/pynlp',
    license='MIT',
    author='Sina',
    author_email='s.aleyaasin@gmail.com',
    description='Python wrapper for Stanford CoreNLP'
)
