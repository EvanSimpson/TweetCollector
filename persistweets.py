

from twython import Twython
import simplejson as json
import time

t = Twython()


category = { "Democratic Party": ["democrat","democrats","democratic", "barack obama", "darcy richardson", "randall terry"], "Republican Party":["republican", "michele bachman", "herman cain", "newt gingrich", "jon huntsman", "gary johnson", "ron paul", "rick perry", "mitt romney", "rick santorum"], "Barack Obama":["barack obama", "obama"], "Darcy Richardson": ["darcy richardson"], "Randall Terry": ["randall terry"], "Michele Bachmann": ["michele bachmann"], "Herman Cain": ["herman cain"], "Newt Gingrich": ["newt gingrich"], "Jon Huntsman": ["jon hunstman"], "Gary Johnson": ["Gary Johnson"], "Ron Paul": ["ron paul"], "Rick Perry": ["rick perry"], "Mitt Romney": ["mitt romney", "romney"], "Rick Santorum": ["rick santorum"] }
search_terms = ["2012 election","presidential election","presidential debate","US president","obama administration","president of the united states","republican","michele bachmann","herman cain","newt gingrich","jon huntsman","gary johnson","ron paul","rick perry","mitt romney","romney","rick santorum","democrat","democrats","democratic","barack obama","obama","darcy richardson","randall terry"]


with open('results.json', 'a') as z:


	for term in search_terms:	
		results = t.search(q = term, lang = "en", result_type = "recent")
		for result in results['results']:
			ob = json.dump(result, z)
			z.write('\n')
	print "Waiting..."
	time.sleep(600)
	print "Resuming..."




print 'end'
