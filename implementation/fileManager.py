import io
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

with open(os.getcwd() + '/config.json', 'r') as config_file:
    config = json.load(config_file)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT = os.getcwd() + '/service_account.json'
PARENT_FOLDER_ID = config['PARENT_FOLDER_ID']


class FileManager:
    '''Represent file managing: uploading and retrieving files from the Google Drive.'''
    def __init__(self):
        pass

    def authenticate(self):
        '''Authenticate the user.'''
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT, scopes=SCOPES)

        return creds

    def create_user_folder(self, service, user_id):
        '''Create a folder for the user if it does not already exist.'''
        query = f"'{PARENT_FOLDER_ID}' in parents and name='{user_id}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])

        if folders:
            return folders[0]['id']

        # Create new folder
        folder_metadata = {
            'name': str(user_id),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [PARENT_FOLDER_ID]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()

        return folder.get('id')

    def upload_file(self, file_path, user_id, date):
        '''Upload the file. Return file id.'''
        creds = self.authenticate()
        service = build('drive', 'v3', credentials=creds)

        # Create or get user folder
        user_folder_id = self.create_user_folder(service, user_id)

        # Format file name
        file_name = f"{user_id}_{date}"

        file_metadata = {
            'name': file_name,
            'parents': [user_folder_id]
        }

        media = MediaFileUpload(file_path)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return file.get('id')

    # def upload_file(self, file_path, user_id, date):
    #     '''Upload the finle. Return file id.'''
    #     creds = self.authenticate()
    #     service = build('drive', 'v3', credentials=creds)
    #
    #     file_metadata = {
    #         'name': 1,
    #         'parents': [PARENT_FOLDER_ID]
    #     }
    #
    #     file = service.files().create(
    #         body=file_metadata,
    #         media_body=file_path,
    #         fields='id'
    #     ).execute()
    #
    #     return file.get('id')

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

    def display_file(self, file_id):
        '''Create the image widget to display.'''
        image_stream = self.stream_image_from_drive(file_id)
        core_image = CoreImage(image_stream, ext="png")
        image_widget = Image(texture=core_image.texture)
        return image_widget

