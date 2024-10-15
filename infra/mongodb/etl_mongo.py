import subprocess
import boto3
import requests
from pymongo import MongoClient
import hcl2
import json
from bson import ObjectId
from datetime import datetime

# Function to get Terraform output in JSON format
s3_client = boto3.client('s3', region_name='us-east-1')
tfvars_file_path = "variable.tf"
tfstate_file = 'terraform.tfstate'

# Load the Terraform state file
with open(tfstate_file, 'r') as file:
    terraform_state = json.load(file)

with open(tfvars_file_path, 'r') as file:
    tfvars = hcl2.load(file)

# with open(tfvars_state, 'r') as file1:
#     tfvars1 = hcl2.load(file1)


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def download_json_from_s3(bucket_name, object_key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    json_data = response['Body'].read().decode('utf-8')
    return json.loads(json_data)


def get_terraform_output():
    # Run 'terraform output -json' command
    result = subprocess.run(['terraform', 'output', '-json'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("Error running terraform:", result.stderr)
        return None

    # Parse JSON output
    return json.loads(result.stdout)

# Function to extract specific output values


def load_data(movie_collection, series_collection, json_file_url, obj):
    print(f"Loading JSON file from: {json_file_url}")

    # Fetch the JSON data
    json_response = requests.get(json_file_url)
    if json_response.status_code == 200:
        json_data = json_response.json()

        # Insert JSON data into MongoDB
        if isinstance(json_data, list):
            movie_collection.insert_many(json_data)
        else:
            movie_collection.insert_one(json_data)
        print(f"Inserted data from {obj['Key']} into MongoDB.")
    else:
        print(
            f"Failed to fetch {json_file_url}: {json_response.status_code}")


def convert_document(doc):
    # Convert "_id" from {"$oid": "..."} to ObjectId
    if "_id" in doc and isinstance(doc["_id"], dict) and "$oid" in doc["_id"]:
        doc["_id"] = ObjectId(doc["_id"]["$oid"])

    # Convert "release_date" from {"$date": {"$numberLong": "..."}} to datetime
    if "release_date" in doc and isinstance(doc["release_date"], dict) and "$date" in doc["release_date"]:
        timestamp = int(doc["release_date"]["$date"]["$numberLong"]) / 1000
        doc["release_date"] = datetime.utcfromtimestamp(timestamp)

    return doc


def mongo_connect(uri, json_file):
    load_var = tfvars.get("variable")
    cluster = ""
    s3_bucket = ""

    # cluster = [data.get("mongo_cluster") for data in load_var]
    for data in load_var:
        try:
            if data.get('mongo_cluster'):
                cluster = data.get("mongo_cluster").get("default")
        except Exception as e:
            pass

# Extract specific resources (e.g., S3 bucket details)
    resources = terraform_state.get('resources', [])
    for resource in resources:
        if resource.get('type') == 'aws_s3_bucket':
            s3_bucket = resource.get('instances', [])[0].get(
                'attributes', {}).get('bucket')
    mongo_client = MongoClient(uri.strip())
    db = mongo_client["MoviesDB"]
    movie_collection = db["movies"]
    series_collection = db["series"]
    my_collection = [movie_collection, series_collection]
    obj_key = ["movies.json", "series.json"]
    print(s3_bucket)
    response = s3_client.list_objects_v2(Bucket=s3_bucket)
    if 'Contents' in response:
        for collection, obj in zip(my_collection, obj_key):
            json_data = download_json_from_s3(s3_bucket, obj)
            cleaned_documents = [
                convert_document(doc) for doc in json_data]
            collection.insert_many(cleaned_documents)
            print("loaded", collection)


def parse_output():
    output = get_terraform_output()

    if output:
        # Extracting the specific outputs (e.g., 'mongo_connection', 'db_user_credentials')
        mongo_connection = output.get("mongo_connection", {}).get("value")
        db_user_credentials = output.get(
            "db_user_credentials", {}).get("value", {})
        username = db_user_credentials.get("username")
        password = db_user_credentials.get("password")
        s3_link = output.get("json_file_urls", {}).get("value")
        # print(s3_link)
        json_file = output.get("json_file_urls", {}).get("value")
        # print(json_file)

        # print(f"MongoDB Connection String: {mongo_connection}")
        mongo_connect(mongo_connection, json_file)
        # print(f"DB Username: {username}")
        # print(f"DB Password: {password}")
    else:
        print("Failed to retrieve Terraform output.")


if __name__ == "__main__":
    parse_output()
