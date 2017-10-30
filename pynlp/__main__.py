from pynlp.config import SERVER_CLASS, DEFAULT_PORT, ENV_NAME
from operator import add
from functools import reduce
import os


def _args(properties):
    def parse(arg): return '-' + str(arg) + ' ' + str(properties[arg]) + ' '
    return reduce(add, map(parse, properties.keys()))


def run_server(port=DEFAULT_PORT, memory=4, timeout=30000):
    java_arg = _args({'cp': '"' + os.environ[ENV_NAME] + '/*"', 'Xmx{}g'.format(memory): ''})
    core_arg = _args({'port': port, 'timeout': timeout})
    os.system('java ' + java_arg + SERVER_CLASS + ' ' + core_arg)


if __name__ == '__main__':
    # TODO: command line arguments.
    run_server()
