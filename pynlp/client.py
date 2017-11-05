from pynlp.config import SERIALIZER_CLASS, DEFAULT_PORT, DEFAULT_ANNOTATORS
import requests
import json
import corenlp_protobuf as core
from pynlp.wrapper import Document


SERIALIZE_PROPS = {
    'outputFormat': 'serialized',
    'serializer': SERIALIZER_CLASS
}

DESERIALIZE_PROPS = {
    'inputFormat': 'serialized',
    'inputSerializer': SERIALIZER_CLASS
}


def _corenlp_request(input_data, props, port=DEFAULT_PORT):
    server = 'http://localhost:{}/'.format(port)
    params = (('properties', json.dumps(props)),)
    return requests.post(url=server, params=params, data=input_data)


def _annotate_binary(text, annotators=DEFAULT_ANNOTATORS, options=None, port=DEFAULT_PORT):
    text = text.encode('utf-8')
    props = dict(SERIALIZE_PROPS, **{'annotators': annotators})
    if options:
        props = dict(props, **options)
    return _corenlp_request(input_data=text, props=props, port=port).content


def _annotate(text, annotators=DEFAULT_ANNOTATORS, options=None, port=DEFAULT_PORT):
    return from_bytes(_annotate_binary(text, annotators, options, port))


def from_bytes(protobuf):
    doc = core.Document()
    core.parseFromDelimitedString(doc, protobuf)
    return doc


# doesn't work.
def to_bytes(proto_doc):
    stream = core.writeToDelimitedString(proto_doc)
    buf = stream.getvalue()
    stream.close()
    return buf


def stanford_core_nlp(annotators=DEFAULT_ANNOTATORS, options=None, port=DEFAULT_PORT):
    def annotate(text):
        return _annotate(text, annotators, options, port)
    return annotate


class StanfordCoreNLP:

    def __init__(self, port=DEFAULT_PORT, annotators=DEFAULT_ANNOTATORS, options=None):
        self._annotators = annotators
        self._options = options
        self._port = port

    def __call__(self, text):
        return self.annotate(text)

    @property
    def annotators(self):
        return self._annotators.split(', ')

    def annotate(self, text):
        return Document(_annotate(text, self._annotators, self._options, self._port))
