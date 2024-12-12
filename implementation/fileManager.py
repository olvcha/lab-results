import io
import json
import os

import fitz
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
    '''Represent file managing: uploading and retrieving files from Google Drive.'''

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

        user_folder_id = self.create_user_folder(service, user_id)
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

    def stream_file_from_drive(self, file_id):
        '''Retrieve the file (image or PDF) and stream it.'''
        creds = self.authenticate()
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        file_stream.seek(0)

        return file_stream

    def get_file_mime_type(self, file_id):
        '''Retrieve the MIME type of the file using the Google Drive API.'''
        creds = self.authenticate()
        service = build('drive', 'v3', credentials=creds)
        file_metadata = service.files().get(fileId=file_id, fields='mimeType').execute()

        return file_metadata['mimeType']

    def convert_pdf_to_images(self, pdf_stream):
        '''Convert PDF stream to images (one image per page) using PyMuPDF.'''
        doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")
        images = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img_data = pix.tobytes()
            images.append(img_data)

        return images

    def display_file(self, file_id):
        '''Create the appropriate widget to display the file (image or PDF).'''

        mime_type = self.get_file_mime_type(file_id)

        if mime_type == 'application/pdf':
            file_stream = self.stream_file_from_drive(file_id)
            images = self.convert_pdf_to_images(file_stream)
            image_widgets = []
            for img_data in images:
                core_image = CoreImage(io.BytesIO(img_data), ext="png")
                image_widget = Image(texture=core_image.texture)
                image_widgets.append(image_widget)

            return image_widgets

        elif mime_type.startswith('image/'):
            file_stream = self.stream_file_from_drive(file_id)
            file_type = mime_type.split('/')[1]
            core_image = CoreImage(file_stream, ext=file_type)
            image_widget = Image(texture=core_image.texture)

            return [image_widget]

        return []
