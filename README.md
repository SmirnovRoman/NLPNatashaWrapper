# NLPNatashaWrapper
Wrapper for NLP library Natasha (txt2json + http server )

depends on https://github.com/natasha

ner2json.py [filename] - converts text file to json with names

ner2json_server.py [port] - listens for requests https://xxx:port/?text=... with reply in json - for running on multiply servers/parallel processing

Example: 

*request*:

http://10.8.0.1:9000/?text=%D0%AF%20%D0%9A%D0%B0%D0%BC%D0%B0%D0%BB%D0%B0%20%D0%A5%D0%B0%D1%80%D1%80%D0%B8%D1%81,%20%D0%BC%D0%BE%D0%B8%20%D0%BC%D0%B5%D1%81%D1%82%D0%BE%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8%D1%8F%20%C2%AB%D0%BE%D0%BD%D0%B0%C2%BB%20%D0%B8%20%C2%AB%D0%B5%D0%B5%C2%BB,%20%D1%8F%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D0%B0,%20%D1%81%D0%B8%D0%B4%D1%8F%D1%89%D0%B0%D1%8F%20%D0%B7%D0%B0%20%D1%81%D1%82%D0%BE%D0%BB%D0%BE%D0%BC%20%D0%B2%20%D1%81%D0%B8%D0%BD%D0%B5%D0%BC%20%D0%BF%D0%B8%D0%B4%D0%B6%D0%B0%D0%BA%D0%B5

*reply*:

{"items":[{"normal":"\u041a\u0430\u043c\u0430\u043b\u0430 \u0425\u0430\u0440\u0440\u0438\u0441","first":"\u041a\u0430\u043c\u0430\u043b\u0430","last":"\u0425\u0430\u0440\u0440\u0438\u0441"}]}



Used for russian youtube/rutube video descriptoin processing 

https://github.com/SmirnovRoman/RussianYoutubeTop






