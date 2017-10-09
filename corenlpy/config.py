PORT = 9000
CORENLP_PATH = '"./stanford-corenlp-full-2017-06-09/*"'

DEFAULT_ANNOTATORS = 'ssplit, tokenize, pos, lemma'

SERIALIZER_CLASS = 'edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer'
SERVER_CLASS = 'edu.stanford.nlp.pipeline.StanfordCoreNLPServer'
