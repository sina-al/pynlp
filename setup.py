from setuptools import setup

with open('./README.md') as file:
    readme = file.read()

setup(
    name='pynlp',
    version='0.4.0',
    packages=['pynlp', 'pynlp.protobuf'],
    install_requires=['requests', 'protobuf'],
    url='http://github.com/sina-al/pynlp',
    license='MIT',
    author='Sina',
    author_email='s.aleyaasin@gmail.com',
    description='Python wrapper for Stanford CoreNLP',
    long_description=readme,
    long_description_content_type='text/markdown',
)
