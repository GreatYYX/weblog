import json
import requests
from bs4 import BeautifulSoup

def generate_500px(user_id):
	url_500px = 'https://500px.com/{}'.format(user_id)
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': url_500px
	}
	resp = requests.get(url_500px, headers=headers)
	if resp.status_code // 100 != 2:
		return
	content = resp.content

	# # local test
	# with open('500px_index.html') as f:
	# 	content = f.read()

	ret = []
	soup = BeautifulSoup(content)
	data = soup.select('#bootstrap_data')[0]
	data = json.loads(data.string.split('\n')[2][len('App.bootstrap = '):])
	for photo in data['userdata']['photos']:
		ret.append({
			'img': photo['image_url'][5],
			'link': 'https://500px.com' + photo['url'],
			'title': photo['name']
		})
	return ret

if __name__ == '__main__':
	output_path = 'content/extra/photos.json'
	user_id = 'yyx'
	with open(output_path, 'w') as fp:
		json.dump(generate_500px(user_id), fp)
