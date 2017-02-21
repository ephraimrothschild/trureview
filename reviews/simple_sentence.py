from spacy.en import English
from reviews import subject_object_extraction as extr
from collections import namedtuple
parser = English()
SimpleSentence = namedtuple('SimpleSentence', ['tokens', 'full_sentence', 'simplified_sentence'])


def extract_simple_sentences(text):
    # simple_tokens = extract_simple_sentences_tokens(text)
    simple_tokens = []
    all_simple_sentences = []
    # Split sentences up
    sentences = text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()

        # Create a parser for the current sentence (this is also considered the 'full_sentence')
        parse = parser(sentence.strip())

        # Find the simplified sub-sentences inside this sentence, and get their tokens.
        # For example, entering the sentence:
        #       "he and his brother shot me and my sister"
        #   will return the following sub-sentence tuples:
        # [('he', 'shot', 'me'), ('he', 'shot', 'sister'), ('brother', 'shot', 'me'), ('brother', 'shot', 'sister')]
        simple = extr.findSVOsTokens(parse)

        # Iterate through each sub-sentence tuple
        for s in simple:
            # Create the SimpleSentence object (this is a named tuple defined at the top of this file)
            # Its structure looks like SimpleSentence(tokens, full_sentence, simplified_sentence)
            simplified_sentence = parser(' '.join([token.lower_ for token in s]))
            simp_sent = SimpleSentence(s, parse, simplified_sentence)
            all_simple_sentences.append(simp_sent)
    return all_simple_sentences


def extract_simple_sentences_tokens(text):
    simp_sents = extract_simple_sentences(text)
    return [simp_sent.tokens for simp_sent in simp_sents]
    # simples = []
    # sentences = text.split('.')
    # for sentence in sentences:
    #     sentence = sentence.strip()
    #     parse = parser(sentence.strip())
    #     simple = extr.findSVOsTokens(parse)
    #     for s in simple:
    #         simples.append(s)
    # return simples


# def extract_simple_sentences(text):
#     simples = []
#     token_tuples = extract_simple_sentences_tokens(text)
#     for token_tuple in token_tuples:
#         simples.append([s.lower_ for s in token_tuple])
#     return simples

def extract_simple_sentences_str(text):
    simples = []
    token_tuples = extract_simple_sentences_tokens(text)
    for token_tuple in token_tuples:
        simples.append(' '.join([s.lower_ for s in token_tuple]))
    return simples


def test():
    text = '''
As a Korean American I am pretty picky when it comes to Korean restaurants. This place is pretty decent. I came here with a group of friends, expecting it to be a typical Korean pub style. It was pretty bright with all the lights turned on and more like a restaurant, which is honestly appropriate as it's next to all the other cute restaurants on 9th.
'''
    text2 = '''
    Food was not delicious, service was good and accommodating. They did not take my reservation when I called ahead to tell them we're on our way, they seemed hesitant on taking reservations. So glad we chose to eat there. Seafood pancake was light and just crisp on the edges, with Bonita flakes still fluttering when served on our table. The rest of the food was very good too. Would eat here again even though parking can be tough to find.
'''
    text3 = '''
    parking be tough
    '''
    print(extract_simple_sentences(text2))

# test()