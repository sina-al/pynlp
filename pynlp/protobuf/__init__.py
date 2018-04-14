# This __init__.py is very heavily inspired from http://github.com/stanfordnlp/python-corenlp-protobuf
# The repo above is out of date but this library is dependent on it.
# Hence, I have an up-to-date implementation here to circumvent dependency headaches

from .CoreNLP_pb2 import Document
from io import BytesIO
from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.internal.decoder import _DecodeVarint


def to_bytes(proto_doc):
    with BytesIO() as stream:
        _EncodeVarint(stream.write, proto_doc.ByteSize(), True)
        stream.write(proto_doc.SerializeToString())
        _bytes = stream.getvalue()
    return _bytes


def from_bytes(bytes_):
    offset = 0
    doc = Document()
    size, pos = _DecodeVarint(bytes_, offset)
    doc.ParseFromString(bytes_[offset + pos:offset + pos + size])
    return doc
