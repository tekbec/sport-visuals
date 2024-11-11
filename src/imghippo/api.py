import os, requests, json

IMGHIPPO_BASE_URL = 'https://api.imghippo.com/v1/'

def upload(image_file: str, title: str | None = None) -> str:
    url = IMGHIPPO_BASE_URL + 'upload'
    files = {'file': (os.path.basename(image_file), open(image_file, 'rb'))}
    data = {
        'api_key': os.environ.get('IMGHIPPO_API_KEY')
    }
    if title: data['title'] = title
    response = requests.post(url, data=data, files=files)
    if response.status_code == 200:
        return json.loads(response.text)['data']['view_url']
    else:
        raise Exception(f'Failed to upload to Imghippo, status code: {str(response.status_code)}')
