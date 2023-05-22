import pymongo
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Access the connection string from the environment variable
connection_string = os.getenv("MONGODB_CONNECTION_STRING")
df = pd.read_csv("../integrated_cleaned/integration_cleaned_definitive.csv")
client = MongoClient("mongodb+srv://mmondini11:maurino@cluster0.xzuticb.mongodb.net/")
db = client["restaurant_db"]
collection = db["restaurant_integrated"]
# Convert the DataFrame to a list of dictionaries
data = df.to_dict(orient="records")
collection.insert_many(data)
