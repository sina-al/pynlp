# pynlp
A *pythonic* wrapper for Stanford CoreNLP.

<p align="center">
        <img src="https://media.giphy.com/media/l2QDNvOnIK6H2CRgY/giphy.gif" >
</p>

## Description
This library provides a Python interface to [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) built over [`corenlp_protobuf`](https://github.com/stanfordnlp/python-corenlp-protobuf). 

## Installation
1. Download Stanford CoreNLP from the official [download page](https://stanfordnlp.github.io/CoreNLP/download.html).
2. Unzip the file and set your `CORE_NLP` environment variable to point to the directory.
3. Install `pynlp` from pip
```
pip3 install pynlp
```

## Usage

### Launch the server
Lauch the `StanfordCoreNLPServer` using the instruction given [here](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html). *Alternatively*, simply run the module.
```
python3 -m pynlp
```
*By default, this lauches the server on localhost using port 9000 and 4gb ram for the JVM. Use the `--help` option for instruction on custom configurations.*

### Example usage

Let's start off with an excerpt from a CNN article.
```python
text = ('GOP Sen. Rand Paul was assaulted in his home in Bowling Green, Kentucky, on Friday, '
        'according to Kentucky State Police. State troopers responded to a call to the senator\'s '
        'residence at 3:21 p.m. Friday. Police arrested a man named Rene Albert Boucher, who they '
        'allege "intentionally assaulted" Paul, causing him "minor injury". Boucher, 59, of Bowling '
        'Green was charged with one count of fourth-degree assault. As of Saturday afternoon, he '
        'was being held in the Warren County Regional Jail on a $5,000 bond.')
```
### Instantiate annotator
Here we demonstrate the following annotators:
* **Annotoators:** *tokenize, ssplit, pos, lemma, ner, entitymentions, coref, sentiment, quote, openie*
* **Options:** *openie.resolve_coref*
```python
from pynlp import StanfordCoreNLP

annotators = 'tokenize, ssplit, pos, lemma, ner, entitymentions, coref, sentiment, quote, openie'
options = {'openie.resolve_coref': 'true'}

nlp = StanfordCoreNLP(annotators=annotators, options=options)

```
### Annotate text
The `nlp` instance is callable. Use it to annotate the text and return a `Document` object.
```python
document = nlp(text)

print(document) # prints 'text'
```
#### Sentence splitting
Let's test the *ssplit* annotator. A `Document` object iterates over its `Sentence` objects.
```python
for index, sentence in enumerate(document):
    print(index, sentence, sep=' )')
```
Output:
```
0) GOP Sen. Rand Paul was assaulted in his home in Bowling Green, Kentucky, on Friday, according to Kentucky State Police.
1) State troopers responded to a call to the senator's residence at 3:21 p.m. Friday.
2) Police arrested a man named Rene Albert Boucher, who they allege "intentionally assaulted" Paul, causing him "minor injury".
3) Boucher, 59, of Bowling Green was charged with one count of fourth-degree assault.
4) As of Saturday afternoon, he was being held in the Warren County Regional Jail on a $5,000 bond.
```
#### Named entity recognition
How about finding all the people mentioned in the document?
```python
[str(entity) for entity in document.entities if entity.type == 'PERSON']
```
Output:
```
Out[2]: ['Rand Paul', 'Rene Albert Boucher', 'Paul', 'Boucher']
```
We may use named entities on a sentence level too.
```python
first_sentence = document[0]
for entity in first_sentence.entities:
    print(entity, '({})'.format(entity.type))
```
Output:
```
GOP (ORGANIZATION)
Rand Paul (PERSON)
Bowling Green (LOCATION)
Kentucky (LOCATION)
Friday (DATE)
Kentucky State Police (ORGANIZATION)
```
#### Part-of-speech tagging
Let's find all the 'VB' tags in the first sentence. A `Sentence` object iterates over `Token` objects.
```python
for token in first_sentence:
    if 'VB' in token.pos:
        print(token, token.pos)
```
Output:
```
was VBD
assaulted VBN
according VBG
```
#### Lemmatization
Using the same words, lets see the lemmas.
```python
for token in first_sentence:
    if 'VB' in token.pos:
       print(token, '->', token.lemma)
```
Output:
```
was -> be
assaulted -> assault
according -> accord
```
#### Coreference resultion
No coreference resolution available in spaCy? No problem. Let's use pynlp to find the first `CorefChain` in the text.
```python
chain = next(document.coref_chains)
print(chain)
```
Output:
```
((GOP Sen. Rand Paul))-[id=4] was assaulted in (his)-[id=5] home in Bowling Green, Kentucky, on Friday, according to Kentucky State Police.
State troopers responded to a call to (the senator's)-[id=10] residence at 3:21 p.m. Friday.
Police arrested a man named Rene Albert Boucher, who they allege "(intentionally assaulted" Paul)-[id=16], causing him "minor injury.
```
In the string representation, coreferences are marked with parenthesis and the referent with double parenthesis.
Each is also labelled with a `coref_id`. Let's have a closer look at the referent.
```python
ref = chain.referent
details = {'type': ref.type, 'number':ref.number, 'animacy': ref.animacy, 'gender':ref.gender}
print(ref, details)

# Note that we can also index coreferences by id
assert chain[4].is_referent
```
Output:
```
GOP Sen. Rand Paul {'type': 'PROPER', 'number': 'SINGULAR', 'animacy': 'ANIMATE', 'gender': 'NEUTRAL'}
```

#### Quotes
Extracting quotes from the text is simple.
```python
list(document.quotes)
```
Output:
```
Out[8]: [<Quote: "intentionally assaulted">]
Out[9]: [<Quote: "minor injury">]

```

*More to come soon...*
