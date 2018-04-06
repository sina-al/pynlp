from . import protobuf


class Document:

    def __init__(self, proto_doc):
        self._doc = proto_doc

    def __str__(self):
        return self._doc.text

    def __len__(self):
        return self._doc.sentence[-1].token[-1].tokenEndIndex

    def __repr__(self):
        return '<{}: [sentences: {}, tokens: {}]>'.format(
            __class__.__name__,
            len(self._doc.sentence),
            self._doc.sentence[-1].token[-1].tokenEndIndex
        )

    def __iter__(self):
        return (Sentence(self._doc, proto_sentence) for proto_sentence in self._doc.sentence)

    def __getitem__(self, item):
        return Sentence(self._doc, self._doc.sentence[item])

    def __eq__(self, other):
        return self._doc == other._doc

    def __bytes__(self):
        return self.to_bytes()

    @property
    def sentences(self):
        return (Sentence(self._doc, proto_sentence) for proto_sentence in self._doc.sentence)

    @property
    def tokens(self):
        return (Token(self._doc, proto_sentence, proto_token)
                for proto_sentence in self._doc.sentence
                for proto_token in proto_sentence.token)

    def to_bytes(self):
        return protobuf.to_bytes(self._doc)

    @classmethod
    def from_bytes(cls, bytes_):
        return cls(protobuf.from_bytes(bytes_))

    @property
    def text(self):
        return self._doc.text

    @property
    def entities(self):
        return [NamedEntity(self._doc, proto_mention) for proto_mention in self._doc.mentions]

    @property
    def coref_chains(self):
        return [CorefChain(self._doc, proto_coref) for proto_coref in self._doc.corefChain]

    def coref_chain(self, chain_id):
        for proto_chain in self._doc.corefChain:
            if proto_chain.chainID == chain_id:
                return CorefChain(self._doc, proto_chain)
        raise IndexError('No CorefChain with id={} exits.'.format(chain_id))

    @property
    def quotes(self):
        return [Quote(self._doc, proto_quote) for proto_quote in self._doc.quote]


class Sentence:

    def __init__(self, proto_doc, proto_sentence):
        self._doc = proto_doc
        self._sentence = proto_sentence

    def __str__(self):
        return ''.join([(t.originalText + t.after) for t in self._sentence.token])

    def __len__(self):
        return len(self._sentence.token)

    def __repr__(self):
        return '<{} : [index: {}, tokens: {}]>'.format(
            __class__.__name__,
            self._sentence.sentenceIndex,
            self._sentence.token[-1].tokenEndIndex
        )

    def __eq__(self, other):
        return self._sentence == other._sentence and self._doc == other._doc

    def __iter__(self):
        return (Token(self._doc, self._sentence, proto_token) for proto_token in self._sentence.token)

    def __getitem__(self, item):
        return Token(self._doc, self._sentence, self._sentence.token[item])

    @property
    def index(self):
        return self._sentence.sentenceIndex

    @property
    def tokens(self):
        return [Token(self._doc, self._sentence, proto_token) for proto_token in self._sentence.token]

    @property
    def entities(self):
        return [NamedEntity(self._doc, proto_mention) for proto_mention in self._sentence.mentions]

    @property
    def sentiment(self):
        return self._sentence.sentiment

    @property
    def coref_mentions(self):
        # todo: implement coref mention (mentionsForCoref)
        raise NotImplementedError('Method under development.')

    @property
    def relations(self):
        # todo: implement relations
        raise NotImplementedError('Method under development.')

    @property  # parseTree, annotatedParseTree, binarizedParseTree
    def parse_tree(self):
        # todo: implement parse tree (ParseTree class?)
        raise NotImplementedError('Method under development.')

    # todo: implement dependencies & e & epp


class Token:

    def __init__(self, proto_doc, proto_sentence, proto_token):
        self._doc = proto_doc
        self._sentence = proto_sentence
        self._token = proto_token

    def __str__(self):
        return self._token.originalText

    def __repr__(self):
        return '<{}: [sentence: {}, index: {}]>'.format(
            __class__.__name__,
            self._sentence.sentenceIndex,
            self._token.beginIndex
        )

    def __eq__(self, other):
        return self._token == other._token and \
               self._sentence == other._sentence and \
               self._doc == other._doc

    def __hash__(self):  # this is not foolproof!
        return hash((self._token.originalText,
                     self._token.beginChar,
                     self._token.endChar))

    @property
    def word(self):
        return self._token.word

    @property
    def ws(self):
        return self._token.after

    @property
    def word_ws(self):
        return self._token.word + self._token.after

    @property
    def pos(self):
        return self._token.pos

    @property
    def ner(self):
        return self._token.ner

    @property
    def lemma(self):
        return self._token.lemma

    @property
    def sentence(self):
        return Sentence(self._doc, self._sentence)


class Root(Token):

    def __init__(self, proto_doc, proto_sentence):
        super().__init__(proto_doc, proto_sentence, None)

    def __eq__(self, other):
        return self._sentence == other._sentence and self._doc == other._doc

    def __hash__(self):
        return hash('ROOT')

    def __str__(self):
        return 'ROOT'

    def __repr__(self):
        return '<Token: [sentence: {}, index: ROOT]>'.format(
            self._sentence.sentenceIndex
        )

    @property
    def word(self):
        return 'ROOT'

    @property
    def word_ws(self):
        return 'ROOT'

    @property
    def pos(self):
        return 'ROOT'

    @property
    def ner(self):
        return 'ROOT'

    @property
    def lemma(self):
        return 'ROOT'


class NamedEntity:

    def __init__(self, proto_doc, proto_mention):
        self._doc = proto_doc
        self._mention = proto_mention
        self._sentence = self._doc.sentence[self._mention.sentenceIndex]
        self._tokens = [token for token in self._sentence.token
                        if token.tokenBeginIndex >= self._mention.tokenStartInSentenceInclusive
                        and token.tokenEndIndex <= self._mention.tokenEndInSentenceExclusive]

    def __str__(self):
        return ' '.join([token.originalText for token in self._tokens])

    def __repr__(self):
        return '<{}: [type: {}, sentence: {}]>'.format(
            __class__.__name__,
            self._mention.entityType,
            self._sentence.sentenceIndex
        )

    def __getitem__(self, item):
        return Token(self._doc, self._sentence, self._tokens[item])

    @property
    def type(self):
        return self._mention.entityType

    @property
    def ner(self):
        return self._mention.ner

    @property
    def normalized_ner(self):
        return self._mention.normalizedNER

    @property
    def wiki_link(self):
        return self._mention.wikipediaEntity

class CorefChain:

    def __init__(self, proto_doc, proto_coref):
        self._doc = proto_doc
        self._coref = proto_coref
        self._index = 0

    def __repr__(self):
        return '<{}: [chain_id: {}, length: {}]>'.format(
            __class__.__name__,
            self._coref.chainID,
            len(self._coref.mention)
        )

    def __str__(self):
        referent = self._coref.mention[self._coref.representative]
        references = {}
        for reference in self._coref.mention:
            references.setdefault(reference.sentenceIndex, []).append(reference)
        string = ''
        for sentence_index in sorted(references):
            words = []
            whitespace = []
            for token in self._doc.sentence[sentence_index].token:
                words.append(token.originalText)
                whitespace.append(token.after)
            for ref in sorted(references[sentence_index], key=lambda r: r.beginIndex):
                left_tag = '('
                right_tag = ')-[id={}]'.format(ref.mentionID)
                if ref.mentionID == referent.mentionID:
                    left_tag = '(' + left_tag
                    right_tag = ')' + right_tag
                words[ref.beginIndex] = left_tag + words[ref.beginIndex]
                words[ref.endIndex - 1] += right_tag

            for index, word in enumerate(words):
                string += word + whitespace[index]

            string += '\n'

        return string

    def __iter__(self):
        return (Coreference(self._doc, self._coref, mention) for mention in self._coref.mention)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise KeyError('Index by coref_id for coreference.')
        for proto_mention in self._coref.mention:
            if proto_mention.mentionID == item:
                return Coreference(self._doc, self._coref, proto_mention)
        raise KeyError('No coreference with id={} exits.'.format(item))

    @property
    def chain_id(self):
        return self._coref.chainID

    @property
    def referent(self):
        proto_coref_mention = self._coref.mention[self._coref.representative]
        return Coreference(self._doc, self._coref, proto_coref_mention)


class Coreference:

    def __init__(self, proto_doc, proto_coref_chain, proto_coref_mention):
        self._doc = proto_doc
        self._coref_chain = proto_coref_chain
        self._coref_mention = proto_coref_mention
        sentence_index = proto_coref_mention.sentenceIndex
        token_span = range(self._coref_mention.beginIndex, self._coref_mention.endIndex)
        self._tokens = [proto_doc.sentence[sentence_index].token[token_index] for token_index in token_span]

    def __repr__(self):
        ref_id = self._coref_chain.mention[self._coref_chain.representative].mentionID
        return '<{}: [coref_id: {}, chain_id: {}, referent: {}]>'.format(
            self.__class__.__name__,
            self._coref_mention.mentionID,
            self._coref_chain.chainID,
            ref_id)

    def __str__(self):
        return ' '.join([token.originalText for token in self._tokens])

    def __getitem__(self, item):
        return Token(self._doc, self._doc.sentence[self._coref_mention.sentenceIndex],
                     self._tokens[item])

    def chain(self):
        return CorefChain(self._doc, self._coref_chain)

    @property
    def is_referent(self):
        referent_id = self._coref_chain.mention[self._coref_chain.representative].mentionID
        return self._coref_mention.mentionID == referent_id

    @property
    def coref_id(self):
        return self._coref_mention.mentionID

    @property
    def type(self):
        return self._coref_mention.mentionType

    @property
    def number(self):
        return self._coref_mention.number

    @property
    def gender(self):
        return self._coref_mention.gender

    @property
    def animacy(self):
        return self._coref_mention.animacy

    @property
    def head(self):
        return self._coref_mention.head


class Quote:

    def __init__(self, proto_doc, proto_quote):
        self._doc = proto_doc
        self._quote = proto_quote

    def __repr__(self):
        return '<{}: {}>'.format(__class__.__name__, self._quote.text)

    def __str__(self):
        return self._quote.text

    def __getitem__(self, item):
        if 0 <= item <= self._quote.sentenceEnd - self._quote.sentenceBegin:
            return Sentence(self._doc,
                            self._doc.sentence[
                                self._quote.sentenceBegin + item
                            ])
        else:
            raise IndexError('Quote contains {} sentences.'.format(
                self._quote.sentenceEnd - self._quote.sentenceBegin + 1
            ))

    @property
    def text(self):
        return self._quote.text[1:-1]

