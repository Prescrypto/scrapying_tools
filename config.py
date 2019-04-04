import os

AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
FOLDER = "<S3 FOLDER>/"
S3_BASE_URL = "https://s3-us-west-2.amazonaws.com/<BUCKET>/<FOLDER>/{}.png"
DB_MAIN_COLLECTION = ""
MONGO_URI = 'mongodb://localhost:27017/'
DEFAULT_DB = ''