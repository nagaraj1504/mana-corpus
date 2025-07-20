import os
import zipfile
from datetime import datetime

def create_backup_zip(source_folder="data", destination_folder="sync"):
    os.makedirs(destination_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"corpus_backup_{timestamp}.zip"
    zip_path = os.path.join(destination_folder, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_folder)
                zipf.write(file_path, arcname)
    return zip_path
