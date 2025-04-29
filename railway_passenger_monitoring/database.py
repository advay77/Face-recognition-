import os
import pymongo
from dotenv import load_dotenv

class MongoDBHandler:
    def __init__(self):
        """Initialize MongoDB connection."""
        load_dotenv()
        
        # Get MongoDB connection string from environment
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DB", "railway_monitoring")
        collection_name = os.getenv("MONGODB_COLLECTION", "detections")
        
        # Connect to MongoDB
        try:
            self.client = pymongo.MongoClient(mongo_uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            
            # Create separate collection for unknown passengers (bonus)
            self.unknown_collection = self.db["unknown_detections"]
            
            print(f"Connected to MongoDB: {db_name}.{collection_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def store_detection(self, detection_data):
        """
        Store encrypted detection data in MongoDB.
        
        Args:
            detection_data (dict): Encrypted detection data
        """
        try:
            result = self.collection.insert_one(detection_data)
            
            # If this is an unknown passenger, also store in the unknown collection
            if detection_data.get("status_encrypted") and "unauthorized" in str(detection_data.get("status_encrypted")):
                self.unknown_collection.insert_one(detection_data)
                
            return result.inserted_id
        except Exception as e:
            print(f"Error storing detection in MongoDB: {e}")
            return None
    
    def close(self):
        """Close the MongoDB connection."""
        if hasattr(self, 'client'):
            self.client.close()