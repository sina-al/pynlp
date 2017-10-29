from enum import Enum


class Doc:  # TODO: parse, depparse, natlog, openie

    def __init__(self, proto_doc):
        self._doc = proto_doc

    def __len__(self):
        return len(self._doc.sentence)

    def __getitem__(self, item):
        return Sentence(self._doc.sentence[item])

    def __str__(self):
        return '\n'.join([str(sentence) for sentence in self])

    @property
    def ents(self):
        for sentence in self._doc.sentence:
            for mention in sentence.mentions:
                yield Mention(sentence, mention)

    def quotes(self):
        for quote in self._doc.quote:
            yield quote.text


class Token:

    def __init__(self, proto_token):
        self._token = proto_token

    def __str__(self):
        return self._token.value

    @property
    def index(self):
        return self._token.beginIndex

    @property
    def orth(self):
        return self._token.word

    @property
    def lemma(self):
        return self._token.lemma

    @property
    def pos(self):
        return self.pos

    @property
    def ent_type(self):
        return self._token.ner

    @property
    def sentiment(self):
        return self._token.sentiment

    @property
    def text(self):
        return self._token.originalText

    @property
    def text_with_ws(self):
        return self.text + self.whitespace

    @property
    def whitespace(self):
        return self._token.after


class Sentence:

    def __init__(self, proto_sentence):
        self._sentence = proto_sentence

    def __len__(self):
        return len(self._sentence.token)

    def __str__(self):
        return ''.join(Token(tok).text_with_ws for tok in self)

    def __getitem__(self, item):
        return Token(self._sentence.token[item])

    def start(self):
        return self._sentence.tokenOffsetBegin

    def end(self):
        return self._sentence.tokenOffsetEnd

    @property
    def start_char(self):
        return self._sentence.characterOffsetBegin

    @property
    def end_char(self):
        return self._sentence.characterOffsetEnd

    @property
    def sentiment(self):
        return self._sentence.sentiment

    @property
    def annotated_parse(self):
        return self._sentence.annotatedParseTree

    @property
    def binarized_parse(self):
        return self._sentence.binarizedParseTree

    @property
    def parse_tree(self):
        return self._sentence.parse_tree

    @property
    def basic_dep(self):
        return self._sentence.basicDependencies

    def enhanced_dep(self):
        return self._sentence.enhancedDependencies

    @property
    def enhanced_pp_dep(self):
        return self._sentence.enhancedPlusPlusDependencies

    @property
    def has_numeric(self):
        return self._sentence.hasNumerizedTokensAnnotation


class Mention:

    def __init__(self, proto_sent, proto_men):
        self._sentence = proto_sent
        self._mention = proto_men
        self._token = self.start

    def __len__(self):
        return self.end - self.start

    def __str__(self):
        return ''.join(Token(self._sentence.token[i]).text_with_ws
                       for i in range(self.start, self.end))

    @property
    def sentence(self):
        return Sentence(self._sentence)

    @property
    def start(self):
        return self._mention.tokenStartInSentenceInclusive

    @property
    def end(self):
        return self._mention.tokenEndInSentenceExclusive

    @property
    def label(self):
        return self._mention.ner

    @property
    def ent_type(self):
        return self._mention.entityType
