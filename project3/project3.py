from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import gutenberg

import nltk


example_text = "Hello Mr.Smith, how are you doing today? The weather is" \
               "great and Python is awesome. The sky is blue. I have too" \
               "much homework to do. 我世人"


# print(sent_tokenize(example_text))
#


# ps = PorterStemmer()
# for word in word_tokenize(example_text):
#     print(ps.stem(word))

# stop_words = set(stopwords.words("english"))
#
# words = word_tokenize(example_text)
#
# filtered_sentence = [w for w in words if w not in stop_words]
#
# print (filtered_sentence)


ps = PorterStemmer()

example_words = ["python", "pythoner", "pythoning", "the", "pythonly"]
for w in example_words:
    print(ps.stem(w))

# words = word_tokenize(example_text)
#
# for w in words:
#     print(ps.stem(w))
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
#
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
#
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         for i in tokenized[5:]:
#             words = word_tokenize(i)
#             tagged = pos_tag(words)
#             # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
#             # chunkGram = r"""Chunk: {<.*>+}
#             #                         }<VB.?|IN|DT|>+{"""
#             # chunkParser = nltk.RegexpParser(chunkGram)
#             # chunked = chunkParser.parse(tagged)
#             # chunked.draw()
#
#             namedEnt = nltk.ne_chunk(tagged)
#             namedEnt.draw()
#
#
#     except Exception as e:
#         print(str(e))
#
# process_content()


lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize("better", pos="a"))
print(lemmatizer.lemmatize("best", pos="a"))
print(lemmatizer.lemmatize("the"))
print(lemmatizer.lemmatize("machin"))


# sample = gutenberg.raw("bible-kjv.txt")
# tok = sent_tokenize(sample)
#
# print(tok[5:15])

# syns = wordnet.synsets("program")
# # synset
# print(syns[0].name())
# # just the word
# print(syns[0].lemmas()[0].name())
#
# # definition
# print(syns[0].definition())
#
# # examples
# print(syns[0].examples())
#
# synonyms = []
# antonyms = []
#
# for syn in wordnet.synsets("good"):
#     for l in syn.lemmas():
#         print("l: ", l)
#         synonyms.append(l.name())
#         if l.antonyms():
#             antonyms.append(l.antonyms()[0].name())

# print(set(synonyms))
# print(set(antonyms))



# semantic similarity

# w1 = wordnet.synset("ship.n.01")
# w2 = wordnet.synset("boat.n.01")
#
# print(w1.wup_similarity(w2))
