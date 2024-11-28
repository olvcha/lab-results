import io
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

with open(os.getcwd() + '/config.json', 'r') as config_file:
    config = json.load(config_file)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT = os.getcwd() + '/service_account.json'
PARENT_FOLDER_ID = config['PARENT_FOLDER_ID']


class FileManager:
    '''Represents file managing: uploading and retrieving files from the Google Drive.'''
    def __init__(self):
        pass

    def authenticate(self):
        '''Authenticate the user.'''
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT, scopes=SCOPES)

        return creds

    def upload_file(self, file_path):
        '''Upload the file. Return file id.'''
        creds = self.authenticate()
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': 1,
            'parents': [PARENT_FOLDER_ID]
        }

        file = service.files().create(
            body=file_metadata,
            media_body=file_path,
            fields='id'
        ).execute()

        return file.get('id')

    def stream_image_from_drive(self, file_id):
        '''Retrieve the image and stream it.'''
        creds = self.authenticate()
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=file_id)
        image_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(image_stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        image_stream.seek(0)
        return image_stream

    def display_image(self, file_id):
        '''Create the image widget to display.'''
        image_stream = self.stream_image_from_drive(file_id)
        core_image = CoreImage(image_stream, ext="png")
        image_widget = Image(texture=core_image.texture)
        return image_widget

#
# fm = FileManager()
# fm.upload_file(os.getcwd() + '/../badanie.png')
