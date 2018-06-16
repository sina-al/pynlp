import unittest
import pynlp
import test.data


class TestStanfordCoreNLP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nlp = pynlp.StanfordCoreNLP(
            host='127.0.0.1',
            port=9000,
            annotators=', '.join([
                'tokenize',
                'ssplit',
                'pos',
                'lemma',
                'ner',
                'entitymentions',
            ])
        )
        cls.document = nlp.annotate_one(text=test.data.TEXT)
        cls.first_sentence = cls.document[0]
        nlp.close()

    def test_ssplit(self):
        actual = [str(token) for token in self.document]
        expected = [

            # Sentence 0
            'GOP Sen. Rand Paul was assaulted in his home in Bowling Green, Kentucky, on Friday,'
            ' according to Kentucky State Police. ',

            # Sentence 1
            "State troopers responded to a call to the senator's residence at 3:21 p.m. Friday. ",

            # Sentence 2
            'Police arrested a man named Rene Albert Boucher, who they allege "intentionally assaulted" '
            'Paul, causing him "minor injury". ',

            # Sentence 3
            'Boucher, 59, of Bowling Green was charged with one count of fourth-degree assault. ',
            'As of Saturday afternoon, he was being held in the Warren County Regional Jail on a $5,000 bond.'
        ]
        self.assertListEqual(expected, actual)

    def test_tokenize(self):
        actual = [str(token) for token in self.first_sentence]
        expected = [
            'GOP', 'Sen.', 'Rand', 'Paul', 'was', 'assaulted', 'in', 'his', 'home', 'in', 'Bowling', 'Green',
            ',', 'Kentucky', ',', 'on', 'Friday', ',', 'according', 'to', 'Kentucky', 'State', 'Police', '.'
        ]
        self.assertListEqual(expected, actual)

    def test_pos(self):
        actual = [token.pos for token in self.first_sentence]
        expected = [
            'NNP', 'NNP', 'NNP', 'NNP', 'VBD', 'VBN', 'IN', 'PRP$', 'NN', 'IN', 'NNP',
            'NNP', ',', 'NNP', ',', 'IN', 'NNP', ',', 'VBG', 'TO', 'NNP', 'NNP', 'NNP', '.'
        ]
        self.assertListEqual(expected, actual)

    def test_lemma(self):
        actual = [token.lemma for token in self.first_sentence]
        expected = [
            'GOP', 'Sen.', 'Rand', 'Paul', 'be', 'assault', 'in', 'he', 'home', 'in', 'Bowling', 'Green',
            ',', 'Kentucky', ',', 'on', 'Friday', ',', 'accord', 'to', 'Kentucky', 'State', 'Police', '.'
        ]
        self.assertListEqual(expected, actual)

    def test_ner(self):
        actual = [token.ner for token in self.first_sentence]
        expected = [
            'ORGANIZATION', 'O', 'PERSON', 'PERSON', 'O', 'O', 'O', 'O', 'O', 'O', 'CITY', 'CITY',
            'O', 'STATE_OR_PROVINCE', 'O', 'O', 'DATE', 'O', 'O', 'O', 'ORGANIZATION', 'ORGANIZATION',
            'ORGANIZATION', 'O'
        ]
        self.assertListEqual(expected, actual)

    def test_entitymentions(self):
        actual = [(entity.type, str(entity)) for entity in self.document.entities]
        expected = [
            ('ORGANIZATION', 'GOP'),
            ('PERSON', 'Rand Paul'),
            ('CITY', 'Bowling Green'),
            ('STATE_OR_PROVINCE', 'Kentucky'),
            ('DATE', 'Friday'),
            ('ORGANIZATION', 'Kentucky State Police'),
            ('PERSON', 'his'),
            ('TITLE', 'senator'),
            ('TIME', '3:21 p.m.'),
            ('DATE', 'Friday'),
            ('PERSON', 'Rene Albert Boucher'),
            ('PERSON', 'Paul'),
            ('PERSON', 'him'),
            ('PERSON', 'Boucher'),
            ('NUMBER', '59'), ('NUMBER', 'one'),
            ('TITLE', 'count'),
            ('CRIMINAL_CHARGE', 'assault'),
            ('DATE', 'Saturday'),
            ('TIME', 'afternoon'),
            ('CITY', 'Warren'),
            ('LOCATION', 'County'),
            ('MONEY', '$ 5,000'),
            ('PERSON', 'he')
        ]
        self.assertListEqual(expected, actual)
