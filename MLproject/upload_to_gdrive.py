import os
import json
import sys
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError  # <--- Ini yang tadi hilang

# --- KONFIGURASI KREDENSIAL ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Ambil kredensial dari Environment Variable (yang diset di GitHub Secrets)
credentials_json = os.environ.get('GDRIVE_CREDENTIALS')

# Cek apakah kredensial ada
if not credentials_json:
    print("Error: Secret 'GDRIVE_CREDENTIALS' tidak ditemukan.")
    # Kita biarkan exit agar ketahuan kalau error
    sys.exit(1)

# Parsing JSON ke variabel dictionary
SERVICE_ACCOUNT_INFO = json.loads(credentials_json)

def upload_to_drive():
    try:
        # --- 1. OTENTIKASI ---
        creds = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        # Nama file saat disimpan di Drive
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"mlruns_backup_{timestamp}.zip"

        # --- 2. ID FOLDER (PENTING!) ---
        # Ganti dengan ID Folder Google Drive Anda
        FOLDER_ID = '0AOIJ3a7U2uOHUk9PVA?hl=id' 
        
        # Metadata file (Nama & Lokasi Folder)
        file_metadata = {
            'name': file_name,
            'parents': [FOLDER_ID] 
        }

        # --- 3. PROSES UPLOAD ---
        # File lokal yang mau diupload
        media = MediaFileUpload('mlruns_backup.zip', mimetype='application/zip')

        print(f"Sedang mengupload {file_name} ke Google Drive...")
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"Sukses! File ID: {file.get('id')}")

    except HttpError as error:
        print(f'Terjadi error saat upload ke GDrive: {error}')
        # Opsional: sys.exit(1) jika ingin workflow jadi Merah (Gagal) saat upload gagal

if __name__ == '__main__':
    upload_to_drive()