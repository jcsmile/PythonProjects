import pymongo
import datetime
import os

def write_to_mongo(documents):
    MONGO_URI = os.getenv('MONGO_URI')
    db_name = 'jobs_db'
    colletion_name = 'job_positions'
    
    try:
        client = pymongo.MongoClient(MONGO_URI)
    # return a friendly error if a URI error is thrown 
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")

    db = client[db_name]
    colletion = db[colletion_name]
    
    if not isinstance(documents, list):
        raise TypeError
    
    try:
        result = colletion.insert_many(documents)
        
        inserted_count = len(result.inserted_ids)
        print("%x documents were inserted." %(inserted_count))

    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")

    except Exception as e:
        print(f'Failed to write to mongoDB {db_name} colletion {colletion_name}, error: {e}')
        
def clean_job_collection():

    try:
        MONGO_URI = os.getenv('MONGO_URI')
        db_name = 'jobs_db'
        colletion_name = 'job_positions'
        
        client = pymongo.MongoClient(MONGO_URI)
        db = client[db_name]
        colletion = db[colletion_name]
        
        colletion.drop()
  
    # return a friendly error if a URI error is thrown 
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    # return a friendly error if an authentication error is thrown
    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")
  
