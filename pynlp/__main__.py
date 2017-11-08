from pynlp.config import SERVER_CLASS, DEFAULT_PORT, ENV_NAME
from argparse import ArgumentParser
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

    parser = ArgumentParser(description='Launch StandfordCoreNLP Server.')

    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        help='port number to server.', default=DEFAULT_PORT)
    parser.add_argument('-m', '--memory', metavar='GB', type=int,
                        help='memory (gb) allocated to JVM.', default=4)
    parser.add_argument('-t', '--timeout', metavar='TIME', type=int,
                        help='server timeout.', default=15000)

    args = parser.parse_args()

    run_server(port=args.port, memory=args.memory, timeout=args.timeout,)
