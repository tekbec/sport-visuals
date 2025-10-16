import os, requests, json
from upyloadthing import UTApi, UTApiOptions

UPLOADTHING_BASE_URL = 'https://api.uploadthing.com'
API = UTApi(UTApiOptions(token=os.environ.get('UPLOADTHING_TOKEN')))

def upload(image_file: str) -> str:
    # Upload a file
    with open(os.path.relpath(image_file), "rb") as f:
        result = API.upload_files(f)
        if not result or len(result) <= 0 or not result[0].url:
            raise Exception(f'Failed to upload to UploadThing.')
        return result[0].url
    raise Exception(f'Failed to upload to UploadThing.')
