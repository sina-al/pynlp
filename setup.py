from setuptools import setup


def long_description():
    with open('./README.md') as file:
        return file.read()


setup(
    name='pynlp',
    version='0.4.1',
    packages=['pynlp', 'pynlp.protobuf'],
    install_requires=['requests', 'protobuf'],
    url='http://github.com/sina-al/pynlp',
    license='MIT',
    author='Sina',
    author_email='s.aleyaasin@gmail.com',
    description='Python wrapper for Stanford CoreNLP',
    long_description=long_description(),
)
