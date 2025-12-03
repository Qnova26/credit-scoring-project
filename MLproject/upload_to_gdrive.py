import os
import json
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

def upload_to_drive():
    try:
        # Authenticate
        creds = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        # Nama file ZIP yang mau diupload
        file_name = f"mlruns_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
        
        # --- PERBAIKAN DI SINI ---
        # Masukkan ID Folder yang tadi Anda copy dari URL
        FOLDER_ID = '1QJ_2pu2w1eDeGoDIgcs-t2nhXh9nDsDF' 
        
        file_metadata = {
            'name': file_name,
            'parents': [FOLDER_ID]  # <-- Ini kuncinya! Kita masukkan ke dalam folder
        }
        # -------------------------

        # ... (sisa kode ke bawah sama)
        media = MediaFileUpload('mlruns_backup.zip', mimetype='application/zip')

        print(f"Mengupload {file_name} ke Google Drive...")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"Sukses! File ID: {file.get('id')}")

    except HttpError as error:
        print(f'An error occurred: {error}')
        # Biarkan script tetap sukses (exit 0) meski gagal upload,
        # agar pipeline tidak merah total (Opsional)
        # sys.exit(1) 

if __name__ == '__main__':
    upload_to_drive()