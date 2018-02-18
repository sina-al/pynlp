from corenlp_protobuf import parseFromDelimitedString
from corenlp_protobuf import writeToDelimitedString
from corenlp_protobuf import Document


def to_bytes(proto_doc):
    stream = writeToDelimitedString(proto_doc)
    _bytes = stream.getvalue()
    stream.close()
    return _bytes


def from_bytes(bytes_):
    doc = Document()
    parseFromDelimitedString(doc, bytes_)
    return doc

