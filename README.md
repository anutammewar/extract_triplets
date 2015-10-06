# extract_triplets
**extract_triplets** is a python program that makes use of stanford parser to extract meaningful entity triplets from sentences of wikipedia pages.
####Example
Consider the sentence "President Obama gave a speech at New Jersey to thousands of people."
The meaningful triplets of entities could be:
* President Obama, gave, speech
* President Obama, gave a speech at, New Jersey
* President Obama, gave a speech to, thousands of people

These triples could help in Natural Language search.

####Dependencies
In order to run the code, the following packages need to be installed first:

1. Wikipedia python library https://github.com/goldsmith/Wikipedia

2. Directory of Stanford coreNLP tool ( http://nlp.stanford.edu/software/corenlp.shtml ) needs to be in the same directory, where the code is being run.

####Usage
Run:
>python extract.py

The program will ask for a wikipedia page title. Let's say the we are looking for "Mumbai", then type "Mumbai" and press return. The program will keep asking for new pages untill given a signal to stop.

####Working

* As an initial step, the program uses Wikipedia library to fetch the wikipedia page of the given title. Then the cleaned text content of the page is extracted using the same library. This text data is used for further processing.
* The coreNLP tool is run on the text data we get from the above step, with the tokenize, ssplit, pos, lemma, ner, parse annotators. After this step we get the text data separated into sentences. For each sentence we get dependency parse tree annotated with Universal Dependency Labels. We make use of these relations for further processing of extracting entities.
* The tool extracts subject-verb-object triples. So first we see if there exist these relations in the parse tree. If all three relations are present then we proceed with the sentence, otherwise we move on to the next sentence. If the three relations are present, we first find out the root-verb and combine the main verb, auxilary verb, adverb, etc to get a complete meaningful single multi-word verb entity. We do the same thing with subject and all possible objects. We also combine vern and its direct object, in case other objects are also present.
* Coreference chains provided by coreNLP can be exploited for improvement.

