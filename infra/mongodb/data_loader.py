import json
import boto3
import requests
from pymongo import MongoClient

# AWS S3 Configuration
BUCKET_NAME = 'my-json-files-bucket-<your-uuid>'
REGION_NAME = 'us-east-1'

# MongoDB Configuration
MONGO_URI = 'mongodb+srv://<db_username>:<db_password>@<your-cluster-name>.mongodb.net/<your-database-name>?retryWrites=true&w=majority'
DATABASE_NAME = 'MovieDB'
MOVIE_COLLECTION_NAME = 'movies'

# Initialize S3 client
s3_client = boto3.client('s3',
                         region_name=REGION_NAME)

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DATABASE_NAME]
collection = db[MOVIE_COLLECTION_NAME]


def load_json_from_s3_and_insert_to_mongo():
    # List all JSON files in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('.json'):
                # Get the URL for the JSON file
                json_file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{obj['Key']}"
                print(f"Loading JSON file from: {json_file_url}")

                # Fetch the JSON data
                json_response = requests.get(json_file_url)
                if json_response.status_code == 200:
                    json_data = json_response.json()

                    # Insert JSON data into MongoDB
                    if isinstance(json_data, list):
                        collection.insert_many(json_data)
                    else:
                        collection.insert_one(json_data)
                    print(f"Inserted data from {obj['Key']} into MongoDB.")
                else:
                    print(
                        f"Failed to fetch {json_file_url}: {json_response.status_code}")


if __name__ == '__main__':
    load_json_from_s3_and_insert_to_mongo()
