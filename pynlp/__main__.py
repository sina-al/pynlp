from argparse import ArgumentParser
from operator import add
from functools import reduce
import os

ENV_NAME = 'CORE_NLP'


def _args(properties):
    def parse(arg): return '-' + str(arg) + ' ' + str(properties[arg]) + ' '
    return reduce(add, map(parse, properties.keys()))


def run_server(port=9000, memory=4, timeout=30000):
    java_arg = _args({'cp': '"' + os.environ[ENV_NAME] + '/*"', 'Xmx{}g'.format(memory): ''})
    core_arg = _args({'port': port, 'timeout': timeout})
    os.system('java {} edu.stanford.nlp.pipeline.StanfordCoreNLPServer {}'.format(java_arg, core_arg))


if __name__ == '__main__':

    parser = ArgumentParser(description='Launch StandfordCoreNLP Server.')

    parser.add_argument('-a', '--address', metavar='ADDR', help='server address',
                        default='localhost')
    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        help='server port number.', default=9000)
    parser.add_argument('-m', '--memory', metavar='GB', type=int,
                        help='memory (gb) allocated to JVM.', default=4)
    parser.add_argument('-t', '--timeout', metavar='TIME', type=int,
                        help='server timeout.', default=15000)

    args = parser.parse_args()

    run_server(port=args.port, memory=args.memory, timeout=args.timeout,)
