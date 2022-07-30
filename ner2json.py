#!/usr/bin/python3
# pip install natasha
import sys
import json
from natasha import (Segmenter, MorphVocab,NewsEmbedding,NewsMorphTagger,NewsSyntaxParser,NewsNERTagger,PER,NamesExtractor,DatesExtractor,MoneyExtractor,AddrExtractor,Doc)
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)
if len(sys.argv)<2:
	print("Not enough args\nusage - ner2json.py txtfilewithtexttoanalyze ")
	sys.exit(-1)
text_file = open(sys.argv[1], "r")
text = text_file.read()
text_file.close()
doc = Doc(text)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)
for token in doc.tokens:
	token.lemmatize(morph_vocab)
doc.parse_syntax(syntax_parser)
doc.tag_ner(ner_tagger)
for span in doc.spans:
    span.normalize(morph_vocab)
for span in doc.spans:
    if span.type == PER:
	    span.extract_fact(names_extractor)
outstr="{\"items\":["
for x in doc.spans:
#	print(x)
	if x.type=='PER':
	    outstr+="{"
	    outstr+="\"normal\":"+json.dumps(x.normal)+","
	    if hasattr(x.fact, 'slots'):
		    for x2 in x.fact.slots:
			    outstr+="\""+x2.key+"\":"+json.dumps(x2.value)+","
	    outstr=outstr.rstrip(",")
	    outstr+="},"
outstr=outstr.rstrip(",")
outstr+="]}"
print(outstr)
