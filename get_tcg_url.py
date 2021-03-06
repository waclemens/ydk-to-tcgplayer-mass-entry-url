import urllib.parse
import pathlib
from collections import Counter
import requests
import json

all_ids = []
exclude_from_ydk = ['#created by ...','#main','#extra','!side']

for path in pathlib.Path('decks').iterdir():
	if path.is_file():
		current_file = open(path, 'r')
		if current_file.name.endswith('.ydk'):
			lines = current_file.read().splitlines()
			ids = [x for x in lines if x not in exclude_from_ydk]
			all_ids.extend(ids)
		current_file.close()

count_ids = Counter(all_ids)
ids = count_ids.keys()
id_param = '?id=' + ','.join(ids)

if not len(ids):
	print('No ids found...')
	exit()

result = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php' + id_param)
card_data = json.loads(result.text)

card_string = ''
for el in card_data['data']:
	card_id = str(el['id'])
	while not count_ids[card_id]:
		card_id = '0' + card_id
	card_string += '||' + str(count_ids[card_id]) + el['name']

url = 'https://www.tcgplayer.com/massentry?productline=Yugioh&c=' + urllib.parse.quote_plus(card_string)
print(url)
