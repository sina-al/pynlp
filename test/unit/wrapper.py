import unittest
from pynlp import protobuf, wrapper


TEST_DATA = './test/data/data-1.dat'


class TestDocument(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA, 'rb') as file:
            cls.proto_doc = protobuf.from_bytes(file.read())

    def setUp(self):
        self.doc = wrapper.Document(self.proto_doc)

    def test_text(self):
        self.assertEqual(self.proto_doc.text, self.doc.text, 'Wrong text.')

    def test_str(self):
        self.assertEqual(self.proto_doc.text, str(self.doc), 'Wrong string')

    def test_repr(self):
        n_sentence = len(self.proto_doc.sentence)
        n_tokens = self.proto_doc.sentence[-1].token[-1].tokenEndIndex
        expected = '<Document: [sentences: {}, tokens: {}]>'.format(n_sentence, n_tokens)
        self.assertEqual(expected, repr(self.doc), 'Wrong representation.')

    def test_length(self):
        length = self.proto_doc.sentence[-1].token[-1].tokenEndIndex
        self.assertEqual(length, len(self.doc), 'Wrong document length.')

    def test_ssplit_iter(self):
        for sentence, proto_sentence in zip(self.doc.sentences, self.proto_doc.sentence):
            self.assertEqual(sentence._sentence, proto_sentence, 'Incorrect sentences.')

    def test_ssplit_item(self):
        n_sentence = len(self.proto_doc.sentence)
        for i in range(n_sentence):
            self.assertEqual(self.proto_doc.sentence[i], self.doc[i]._sentence, 'Incorrect sentences.')

    def test_equality(self):
        other = wrapper.Document(self.proto_doc)
        self.assertTrue(self.doc == other, 'Invalid equality.')

    def test_to_bytes(self):
        self.assertEqual(protobuf.to_bytes(self.proto_doc), self.doc.to_bytes())

    def test_entities(self):
        for entity, proto_mention in zip(self.doc.entities, self.proto_doc.mentions):
            self.assertEqual(entity._mention, proto_mention, 'Incorrect named entity.')

    def test_coref_chains(self):
        for coref, proto_coref in zip(self.doc.coref_chains, self.proto_doc.corefChain):
            self.assertEqual(coref._coref, proto_coref, 'Incorrect coref chain.')

    def test_coref_chain(self):
        for coref in self.proto_doc.corefChain:
            self.assertEqual(coref, self.doc.coref_chain(coref.chainID)._coref, 'Incorrect coref.')

    def test_quotes(self):
        for proto_quote, quote in zip(self.proto_doc.quote, self.doc.quotes):
            self.assertEqual(proto_quote, quote._quote, 'Incorrect quote.')


class TestSentence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA, 'rb') as file:
            cls.proto_doc = protobuf.from_bytes(file.read())
            cls.proto_sentence = cls.proto_doc.sentence[0]

    def setUp(self):
        self.sentence = wrapper.Sentence(self.proto_doc, self.proto_sentence)

    def test_len(self):
        self.assertEqual(len(self.proto_sentence.token), len(self.sentence), 'Sentence length wrong.')

    def test_repr(self):
        index = self.proto_sentence.sentenceIndex
        tokens = self.proto_sentence.token[-1].tokenEndIndex
        expect = '<Sentence : [index: {}, tokens: {}]>'.format(index, tokens)
        self.assertEqual(expect, repr(self.sentence))

    def test_equality(self):
        other = wrapper.Sentence(self.proto_doc, self.proto_sentence)
        self.assertTrue(other == self.sentence, 'Invalid equality')

    def test_tokenize_iter(self):
        for token, proto_token in zip(self.sentence, self.proto_sentence.token):
            self.assertEqual(token._token, proto_token, 'Incorrect token.')

    def test_tokenize_item(self):
        n_token = len(self.proto_sentence.token)
        for i in range(n_token):
            self.assertEqual(self.sentence.tokens[i]._token, self.proto_sentence.token[i])

    def test_index(self):
        self.assertEqual(self.sentence.index, self.proto_sentence.sentenceIndex)

    def test_entities(self):
        for entity, proto_mention in zip(self.sentence.entities, self.proto_sentence.mentions):
            self.assertEqual(entity._mention, proto_mention, 'Incorrect named entity.')

    def test_sentiment(self):
        self.assertEqual(self.sentence.sentiment, self.proto_sentence.sentiment)

    # todo: test e/epp/dependencies, coref_mentions, relaations, parse_tree


class TestToken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA, 'rb') as file:
            cls.proto_doc = protobuf.from_bytes(file.read())
            cls.proto_sentence = cls.proto_doc.sentence[0]

    def setUp(self):
        self.proto_tokens = [t for t in self.proto_sentence.token]
        self.tokens = (wrapper.Token(self.proto_doc, self.proto_sentence, proto_token)
                       for proto_token in self.proto_tokens)

    def test_str(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(proto_token.originalText, str(token))

    def test_repr(self):
        s = self.proto_sentence.sentenceIndex
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            i = proto_token.beginIndex
            expect = '<Token: [sentence: {}, index: {}]>'.format(s, i)
            self.assertEqual(expect, repr(token))

    def test_equality(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            other = wrapper.Token(self.proto_doc, self.proto_sentence, proto_token)
            self.assertTrue(other == token)

    def test_hash(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            expect = hash(tuple(getattr(proto_token, attr) for attr in ('originalText', 'beginChar', 'endChar')))
            self.assertEqual(expect, hash(token))

    def test_word(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(proto_token.word, token.word)

    def test_ws(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(proto_token.after, token.ws)

    def test_word_ws(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(proto_token.word + proto_token.after, token.word_ws)

    def test_pos(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(token.pos, proto_token.pos)

    def test_ner(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(token.ner, proto_token.ner)

    def test_lemma(self):
        for proto_token, token in zip(self.proto_tokens, self.tokens):
            self.assertEqual(token.lemma, proto_token.lemma)

    def test_sentence(self):
        for token in self.tokens:
            self.assertEqual(token.sentence._sentence, self.proto_sentence)

# todo: unit test root token


class TestNamedEntity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA, 'rb') as file:
            cls.proto_doc = protobuf.from_bytes(file.read())

    def setUp(self):
        self.proto_mentions = [m for m in self.proto_doc.mentions]
        self.entities = (wrapper.NamedEntity(self.proto_doc, proto_mention)
                         for proto_mention in self.proto_mentions)

    # todo: test named entity repr + str + getitem

    def test_type(self):
        for entity, proto_mention in zip(self.entities, self.proto_mentions):
            self.assertEqual(entity.type, proto_mention.entityType, 'Entity types not equal.')

    def test_ner(self):
        for entity, proto_mention in zip(self.entities, self.proto_mentions):
            self.assertEqual(entity.ner, proto_mention.ner, 'NER not equal')

    def test_normalized_ner(self):
        for entity, proto_mention in zip(self.entities, self.proto_mentions):
            self.assertEqual(entity.normalized_ner, proto_mention.normalizedNER, 'NER not equal')

# todo: test corefchain
# todo: test coreference
# todo: test quote


if __name__ == '__main__':
    unittest.main()
