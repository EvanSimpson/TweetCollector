import simplejson as json

def characterize_set(thing, hist):
	for i in thing:
		hist[i] = hist.get(i, 0) + 1

if __name__ == "__main__":
	with open('debateday3.json', 'r') as z:
		hist = {}
		for line in z:
			jstweet = json.loads(line)
			characterize_set(jstweet, hist)
		print hist