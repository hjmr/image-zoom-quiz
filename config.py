class Config:
    ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg', '.JPG', '.png', '.PNG'])
    MAX_IMAGE_WIDTH = 1280
    UPLOAD_FOLDER = 'uploaded'
    DB_FILE = 'image_db.sqlite3'
