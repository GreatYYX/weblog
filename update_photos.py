"""Sync public photos from 500px into the site.

500px image URLs are signed and expire after ~2 days, so instead of saving
those URLs we download each image into content/statics/gallery/ and write
content/extra/photos.json pointing at the local copies.

Usage: python update_photos.py
"""
import json
import os
import urllib.request

USERNAME = 'yyx'
API = 'https://api-neo.500px.com/graphql'
IMG_DIR = 'content/statics/gallery'
IMG_URL_PREFIX = '/statics/gallery'
OUTPUT_PATH = 'content/extra/photos.json'
PAGE_SIZE = 50
HEADERS = {
    'Content-Type': 'application/json',
    'x-500px-platform': 'web',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
}

USER_QUERY = 'query($username:String!){getUser(username:$username){id}}'
PHOTOS_QUERY = '''
query($userId:ID!,$first:Int!,$after:String){
  pageResources(userId:$userId,first:$first,after:$after,
                resourceTypes:[PHOTO],sort:CREATED_AT_DESC){
    edges{node{__typename ... on Photo{
      id title isPrivate isDeleted urls{size_2048}
    }}}
    pageInfo{hasNextPage endCursor}
  }
}'''


def graphql(query, variables):
    body = json.dumps({'query': query, 'variables': variables}).encode()
    req = urllib.request.Request(API, data=body, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get('errors'):
        raise RuntimeError(payload['errors'])
    return payload['data']


def fetch_photos(username):
    user = graphql(USER_QUERY, {'username': username})['getUser']
    if not user:
        raise RuntimeError('500px user not found: {}'.format(username))
    photos, after = [], None
    while True:
        page = graphql(PHOTOS_QUERY, {
            'userId': user['id'], 'first': PAGE_SIZE, 'after': after,
        })['pageResources']
        for edge in page['edges']:
            node = edge['node']
            if (node.get('__typename') == 'Photo' and not node['isPrivate']
                    and not node['isDeleted'] and node['urls']['size_2048']):
                photos.append(node)
        if not page['pageInfo']['hasNextPage']:
            return photos
        after = page['pageInfo']['endCursor']


def download(url, path):
    req = urllib.request.Request(url, headers={'User-Agent': HEADERS['User-Agent']})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    tmp = path + '.part'
    with open(tmp, 'wb') as fp:
        fp.write(data)
    os.replace(tmp, path)


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    photos = fetch_photos(USERNAME)

    ret, keep = [], set()
    for photo in photos:
        filename = '{}.jpg'.format(photo['id'])
        keep.add(filename)
        path = os.path.join(IMG_DIR, filename)
        if not os.path.exists(path):
            print('download', filename, photo['title'].strip())
            download(photo['urls']['size_2048'], path)
        ret.append({
            'img': '{}/{}'.format(IMG_URL_PREFIX, filename),
            'link': 'https://500px.com/photo/{}'.format(photo['id']),
            'title': photo['title'].strip(),
        })

    # remove local copies of photos that were deleted or made private on 500px
    for filename in os.listdir(IMG_DIR):
        if filename.endswith('.jpg') and filename not in keep:
            print('remove', filename)
            os.remove(os.path.join(IMG_DIR, filename))

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as fp:
        json.dump(ret, fp, indent=4, ensure_ascii=False)
    print('{} photos written to {}'.format(len(ret), OUTPUT_PATH))


if __name__ == '__main__':
    main()
