from corenlpy.config import PORT, CORENLP_PATH
import os
from operator import add
from functools import reduce


CLASS = {
    'server': 'edu.stanford.nlp.pipeline.StanfordCoreNLPServer',
    'protobuf': 'edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer'
}

MEMORY = 4


def _args(properties):
    def parse(arg): return '-' + str(arg) + ' ' + str(properties[arg]) + ' '
    return reduce(add, map(parse, properties.keys()))


def _run_server(memory, port, timeout=5000):
    java_arg = _args({'cp': CORENLP_PATH, 'Xmx{}g'.format(memory): ''})
    core_arg = _args({'port': port, 'timeout': timeout})
    os.system('java ' + java_arg + CLASS['server'] + ' ' + core_arg)


if __name__ == '__main__':
    _run_server(MEMORY, PORT)
