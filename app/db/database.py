import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

# Load environment variables
load_dotenv()

# Get credentials from environment variables
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

# Connect to your Azure Cosmos DB
try:
    db_client = MongoClient(MONGO_CONNECTION_STRING)
    db = db_client["expensesdb"]
    collection = db["entries"]
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    # You might want to handle this more gracefully, e.g., by exiting
    db_client = None
    collection = None

# A simple utility method to confirm the database connection
def test_connection():
    """
    Tests the MongoDB connection by sending a ping command.
    Returns True if connection is successful, False otherwise.
    """
    print("Before DB Connection..........!", db_client)
    if not db_client:
        return False
    try:
        db_client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False