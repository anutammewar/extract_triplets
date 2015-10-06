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

