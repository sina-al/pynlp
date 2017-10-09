from corenlpy.config import DEFAULT_ANNOTATORS, SERIALIZER_CLASS, PORT
import requests
import json
import corenlp_protobuf as core


SERIALIZE_PROPS = {
    'outputFormat': 'serialized',
    'serializer': SERIALIZER_CLASS
}

DESERIALIZE_PROPS = {
    'inputFormat': 'serialized',
    'inputSerializer': SERIALIZER_CLASS
}


def _corenlp_request(input_data, props, port=PORT):
    server = 'http://localhost:{}/'.format(port)
    params = (('properties', json.dumps(props)),)
    return requests.post(url=server, params=params, data=input_data)


def annotate(text, annotators=DEFAULT_ANNOTATORS, port=PORT):
    props = dict(SERIALIZE_PROPS, **{'annotators': annotators})
    return _corenlp_request(input_data=text, props=props, port=port).content


def re_annotate(serialized, annotators=DEFAULT_ANNOTATORS, port=PORT):
    io = dict(SERIALIZE_PROPS, **DESERIALIZE_PROPS)
    props = dict(io, **{'annotators': annotators})
    return _corenlp_request(input_data=serialized, props=props, port=port).content


class StanfordCoreNLP:

    def __init__(self, port=PORT, annotators=DEFAULT_ANNOTATORS):
        self._annotators = annotators
        self.port = port

    def __call__(self, *args, **kwargs):
        docs = [self.annotate(doc) for doc in args]
        return docs if len(docs) > 1 else docs[0]

    @property
    def annotators(self):
        return self._annotators.split(', ')

    def annotate(self, document):
        doc = core.Document()
        proto = annotate(document.encode('UTF-8'), self._annotators)
        core.parseFromDelimitedString(doc, proto)
        return doc

