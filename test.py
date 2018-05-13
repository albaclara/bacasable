# -*-coding:Utf-8 -*
import unicodedata 

villenormalisee = unicodedata.normalize('NFD', 'vert').encode('ascii', 'ignore') 

print(villenormalisee)
villenormalisee = unicodedata.normalize('NFD', 'vèrt').encode('ascii', 'ignore') 

print(villenormalisee)
