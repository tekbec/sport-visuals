import os, requests, json

IMGUR_BASE_URL = 'https://api.imgur.com/3/'

def upload(image_file: str, title: str | None = None, description: str | None = None) -> str:
    url = IMGUR_BASE_URL + 'image'
    files = {'image': (os.path.basename(image_file), open(image_file, 'rb'))}
    data = {}
    if title: data['title'] = title
    if description: data['description'] = description
    headers = {
        'Authorization': f'Client-ID {os.environ.get('IMGUR_CLIENT_ID')}'
    }
    response = requests.post(url, data=data, files=files, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)['data']['link']
    else:
        raise Exception(f'Failed to upload to imgur, status code: {str(response.status_code)}')
