import firebase_admin
from firebase_admin import credentials, storage
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Firebase (if not already initialized)
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred, {
        'storageBucket': os.getenv("STORAGE_BUCKET")
    })

# Upload a file
def upload_file(local_file_path, destination_blob_name):
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(local_file_path)

    # Make the blob publicly accessible (optional)
    blob.make_public()

    print(f"File uploaded to: {blob.public_url}")
    return blob.public_url

# Test upload
if __name__ == "__main__":
    # Get filename from command line argument or use default
    if len(sys.argv) > 1:
        local_image = sys.argv[1]
    else:
        print("Usage: python test_upload.py <image_file_path>")
        print("Example: python test_upload.py 'sam ibrahim building.jpg'")
        sys.exit(1)

    # Check if file exists
    if not os.path.exists(local_image):
        print(f"Error: File '{local_image}' not found")
        sys.exit(1)

    # Append timestamp to filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename, ext = os.path.splitext(os.path.basename(local_image))
    destination_name = f"{filename}_{timestamp}{ext}"

    storage_url = upload_file(local_image, destination_name)
    print(f"Storage URL: {storage_url}")
