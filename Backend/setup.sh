# Define the file path and Google Drive file ID
FILE="your_downloaded_file.ext"
FILE_ID="1Jx2m_2I1d9PYzFRQ4gl82xQa-G7Vsnsl"

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "File not found. Downloading..."
    gdown "$FILE_ID"
else
    echo "File already exists. Skipping download."
fi

# Continue with the rest of your setup
python3 -m pip install -e ../.
python3 manage.py makemigrations account translation
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
