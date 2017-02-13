import os, re
import json
import pdb
import collections
from bs4 import BeautifulSoup
from django.utils.text import slugify

sourceLink = 'http://www.gitasupersite.iitk.ac.in/'
source = 'Gita Supersite'

works = [{
	'originalTitle': "भगवद्गीता",
	'englishTitle': "Bhagavad Gita",
	'author': "Not available",
	'dirname': "bhagavadgita",
	'source': source,
	'sourceLink': sourceLink,
	'language': 'sanskrit',
	'text': {},
}, {
	'originalTitle': "ब्रह्म सूत्र",
	'englishTitle': "Brahma Sutras",
	'author': "Not available",
	'dirname': "brahmasutra",
	'source': source,
	'sourceLink': sourceLink,
	'language': 'sanskrit',
	'text': {},
}, {
	'originalTitle': "रामायणम्",
	'englishTitle': "Ramayana",
	'author': "Not available",
	'dirname': "ramayana",
	'source': source,
	'sourceLink': sourceLink,
	'language': 'sanskrit',
	'text': {},
}, {
	'originalTitle': "श्रीरामचरितमानस",
	'englishTitle': "Ramcharitmanas",
	'author': "Not available",
	'dirname': "ramcharitmanas",
	'source': source,
	'sourceLink': sourceLink,
	'language': 'sanskrit',
	'text': {},
}, {
	'originalTitle': "Yoga Sūtras of Patañjali",
	'englishTitle': "Yoga Sūtras of Patañjali",
	'author': "Not available",
	'dirname': "yogasutra",
	'source': source,
	'sourceLink': sourceLink,
	'language': 'sanskrit',
	'text': {},
}]

ramayanaTexts = ['aranyakanda', 'ayodhyakanda', 'balakanda', 'kishkindakanda', 'sundarakanda']
ramcharitmanasTexts = ['aranya_kaanda', 'ayodhya_kaanda', 'baal_kaanda', 'kishkindha_kaanda', 'lanka_kaanda', 'sundara_kaanda', 'uttara_kaanda']

def jaggedListToDict(text):
	node = { str(i): t for i, t in enumerate(text) }
	node = collections.OrderedDict(sorted(node.items(), key=lambda k: int(k[0])))
	for child in node:
		if isinstance(node[child], list):
			node[child] = jaggedListToDict(node[child])
	return node

def fileToLines(root, fname):
	with open(os.path.join(root, fname)) as f:
		lines = f.read().splitlines()

	text = []
	for line in lines:
		if len(line.strip()):
			text.append(line)

	return text

def main():
	if not os.path.exists('cltk_json'):
		os.makedirs('cltk_json')
	# Build json docs from txt files
	for root, dirs, files in os.walk("."):
		path = root.split('/')
		print((len(path) - 1) * '---', os.path.basename(root))

		for fname in files:
			if fname.endswith('.txt'):
				print((len(path)) * '---', fname)

				for work in works:
					if path[1] == work['dirname']:

						if work['dirname'] == 'bhagavadgita':
							chapter = int(fname.replace('chapter_', '').replace('_sanskrit.txt', '')) - 1
							text = fileToLines(root, fname)
							work['text'][str(chapter)] = jaggedListToDict(text)
							work['text'] = collections.OrderedDict(sorted(work['text'].items(), key=lambda k: int(k[0])))

						elif work['dirname'] == 'brahmasutra':
							chapter = str(int(path[2].replace('chapter_', '')) - 1)
							quarter = str(int(path[3].replace('quarter_', '')) - 1)
							text = fileToLines(root, fname)

							if chapter not in work['text']:
								work['text'][chapter] = {}
							if quarter not in work['text'][chapter]:
								work['text'][chapter][quarter] = {}
							work['text'][chapter][quarter] = jaggedListToDict(text)
							work['text'] = collections.OrderedDict(sorted(work['text'].items(), key=lambda k: int(k[0])))
							work['text'][chapter] = collections.OrderedDict(sorted(work['text'][chapter].items(), key=lambda k: int(k[0])))

						elif work['dirname'] == 'ramayana':
							text = fileToLines(root, fname)
							chapter = str(ramayanaTexts.index(fname.replace("_sanskrit.txt", "")))

							if chapter not in work['text']:
								work['text'][chapter] = {}

							work['text'][chapter] = jaggedListToDict(text)
							work['text'] = collections.OrderedDict(sorted(work['text'].items(), key=lambda k: int(k[0])))

						elif work['dirname'] == 'ramcharitmanas':
							text = fileToLines(root, fname)
							chapter = str(ramcharitmanasTexts.index(path[2]))
							if fname == 'chopayi.txt':
								quarter = '0'
							elif fname == 'doha.txt':
								quarter = '1'

							if chapter not in work['text']:
								work['text'][chapter] = {}
							if quarter not in work['text'][chapter]:
								work['text'][chapter][quarter] = {}

							work['text'][chapter] = jaggedListToDict(text)
							work['text'] = collections.OrderedDict(sorted(work['text'].items(), key=lambda k: int(k[0])))
							work['text'][chapter] = collections.OrderedDict(sorted(work['text'][chapter].items(), key=lambda k: int(k[0])))

						elif work['dirname'] == 'yogasutra':
							text = fileToLines(root, fname)
							chapter = str(int(path[2].replace('chapter_', '')) - 1)
							if fname == 'bhashya.txt':
								quarter = '0'
							elif fname == 'bhojavruthi.txt':
								quarter = '1'
							elif fname == 'sutra.txt':
								quarter = '2'

							if chapter not in work['text']:
								work['text'][chapter] = {}
							if quarter not in work['text'][chapter]:
								work['text'][chapter][quarter] = {}

							work['text'][chapter] = jaggedListToDict(text)
							work['text'] = collections.OrderedDict(sorted(work['text'].items(), key=lambda k: int(k[0])))
							work['text'][chapter] = collections.OrderedDict(sorted(work['text'][chapter].items(), key=lambda k: int(k[0])))


	for work in works:
		fname = slugify(work['source']) + '__' + slugify(work['englishTitle'][0:100]) + '__' + slugify(work['language']) + '.json'
		fname = fname.replace(" ", "")
		with open('cltk_json/' + fname, 'w') as f:
			json.dump(work, f)

if __name__ == '__main__':
	main()
