import os
import json
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

def upload_to_drive():
    # 1. Ambil Credentials dari GitHub Secrets
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    folder_id = os.environ.get('GDRIVE_FOLDER_ID')

    if not creds_json or not folder_id:
        print("Error: GDRIVE_CREDENTIALS atau GDRIVE_FOLDER_ID tidak ditemukan.")
        return

    # Parse JSON string ke Dictionary
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)

    # 2. Build Service Drive
    service = build('drive', 'v3', credentials=creds)

    # 3. Zip Folder mlruns agar mudah diupload
    # Folder yang mau di-zip
    source_dir = "mlruns"
    # Nama file output (misal: mlruns_2023-10-27_10-30-00)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"mlruns_backup_{timestamp}"
    
    print(f"Sedang mengompres folder {source_dir}...")
    shutil.make_archive(output_filename, 'zip', source_dir)
    zip_file = output_filename + ".zip"

    # 4. Upload ke Google Drive
    print(f"Mengupload {zip_file} ke Google Drive...")
    
    file_metadata = {
        'name': zip_file,
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(zip_file, mimetype='application/zip')
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Sukses! File ID: {file.get('id')}")

if __name__ == "__main__":
    upload_to_drive()