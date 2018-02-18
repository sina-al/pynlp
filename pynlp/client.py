from .exceptions import CoreNLPServerError
from .serializers import PROTOBUF
from .wrapper import Document
from requests import Session
import corenlp_protobuf
import json


_BOOL_MAP = {True: 'true', False: 'false'}


class Properties:

    def __init__(self,
                 input_format,
                 input_serializer,
                 output_format,
                 output_serializer,
                 annotators,
                 options,):

        if input_format:
            assert input_serializer
            self.inputFormat = input_format
            self.inputSerializer = input_serializer

        if output_format == 'serialized':
            assert output_serializer
            self.serializer = output_serializer

        self.outputFormat = output_format

        if annotators:
            self.annotators = ', '.join(annotators)

        for option, value in (options or {}).items():
            if option.split('.')[0] in annotators:
                if value in _BOOL_MAP:
                    value = _BOOL_MAP[value]
                setattr(self, option, value)

    def __str__(self):
        return json.dumps(self.__dict__)

    @classmethod
    def text_to_protobuf(cls, annotators, options):
        return cls(input_format=None,
                   input_serializer=None,
                   output_format='serialized',
                   output_serializer=PROTOBUF,
                   annotators=annotators,
                   options=options)

    @classmethod
    def protobuf_to_protobuf(cls, annotators, options):  # For appending annotations
        return cls(input_format='serialized',
                   input_serializer=PROTOBUF,
                   output_format='serialized',
                   output_serializer=PROTOBUF,
                   annotators=annotators,
                   options=options)


class CoreNLPClient(Session):

    def __init__(self, properties: Properties):
        super().__init__()
        self._handler = None
        if properties.outputFormat == 'serialized':
            if properties.serializer == PROTOBUF:
                self._handler = '_protobuf'
            else:
                raise NotImplementedError('serializer not supported: "{}"'.format(properties.serializer))
        elif properties.outputFormat == 'json':
            self._handler = '_json'
        else:
            raise NotImplementedError('outputFormat not supported: "{}"'.format(properties.outputFormat))
        assert self._handler

    def request(self, *args, **kwargs):
        response = super(CoreNLPClient, self).request(*args, **kwargs)
        return self._handle(response)

    def _handle(self, response):
        if response.ok:
            return getattr(self, self._handler)(response)
        else:
            return self._bad_response(response)

    @staticmethod
    def _bad_response(response):
        status = response.status_code
        text = response.text
        raise CoreNLPServerError('Status code: [{}] ({}) '.format(status, text))

    @staticmethod
    def _protobuf(response):
        proto_doc = corenlp_protobuf.Document()
        corenlp_protobuf.parseFromDelimitedString(proto_doc, response.content)
        return proto_doc

    @staticmethod
    def _json(response):
        try:
            return response.json()
        except ValueError:
            raise CoreNLPServerError('Invalid json.')

    @staticmethod
    def _xml(response):
        raise NotImplementedError('Under development.')  # TODO: xml output_format

    @staticmethod
    def _text(response):
        return response.text


class StanfordCoreNLP:

    def __init__(self, host='127.0.0.1', port=9000, annotators=None, options=None):
        if annotators:
            annotators = annotators.split(',')
        self._properties = Properties.text_to_protobuf(annotators, options)
        self._address = "http://{}:{}/".format(host, port)
        self._client = CoreNLPClient(self._properties)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __call__(self, texts, **kwargs):
        return self.annotate_one(texts)

    def _annotate(self, text):
        return self._client.post(url=self._address, data=text, params=(('properties', str(self._properties)),))

    def annotate_one(self, text):
        return Document(self._annotate(text))

    def close(self):
        self._client.close()


def stanford_corenlp(host='127.0.0.1', port=9000, annotators=None, options=None):
    if annotators:
        annotators = annotators.split(',')
    props = Properties.text_to_protobuf(annotators, options)
    client = CoreNLPClient(props)

    def nlp(text):
        return client.post(url="http://{}:{}/".format(host, port),
                           params=(('properties', str(props)),),
                           data=text,)
    return nlp
