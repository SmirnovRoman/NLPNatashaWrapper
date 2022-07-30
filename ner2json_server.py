#!/usr/bin/python3
# pip install natasha
import sys
import json
from natasha import (Segmenter, MorphVocab,NewsEmbedding,NewsMorphTagger,NewsSyntaxParser,NewsNERTagger,PER,NamesExtractor,DatesExtractor,MoneyExtractor,AddrExtractor,Doc)

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import urllib.parse

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
	print("Not enough args\nusage - ner2json_server.py port")
	sys.exit(-1)



def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', int(sys.argv[1]))
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    """do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/json")
        self.end_headers()
        text = str(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('text',None))
        print(text)
#	text_file = open(sys.argv[1], "r")
#	text = text_file.read()
#	text_file.close()
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
#        <html><head><meta charset="utf-8">'.encode())
#        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode())
#        self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode())
#	print(outstr)
        self.wfile.write(outstr.encode())

run(handler_class=HttpGetHandler)


