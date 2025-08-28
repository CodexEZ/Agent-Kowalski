from fastmcp import FastMCP, Client
from pymongo import MongoClient
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
import os
from dotenv import load_dotenv
from bson import ObjectId
import sys
from loguru import logger
import json
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
load_dotenv()

app = FastMCP()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("mcp_db")

def clean_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: str(v) if isinstance(v, ObjectId) else v
        for k, v in doc.items()
    }


# Get list of all databases
@app.tool(
    description="Fetch a list of all available databases in the MongoDB server."
)
def get_databases() -> Dict[str, List[str]]:
    logger.info("GET DATABASES")
    return {"databases": client.list_database_names()}


# Get collections inside a specific database
@app.tool(
    description="Fetch all collection (table) names inside a given database."
)
def get_collections(database: str) -> Dict[str, Any]:
    logger.info("GET COLLECTIONS")
    db = client[database]
    return {
        "database": database,
        "collections": db.list_collection_names()
    }

@app.tool(description="Fetch the required fields in a collection")
def get_fields_for_collection(database: str, collection: str) -> Dict[str, Any]:
    logger.info("GET SCHEMA")
    db = client[database]
    collection_obj = db[collection]
    
    # Get one sample document to infer fields
    record = collection_obj.find_one()
    if not record:
        return {
            "database": database,
            "collection": collection,
            "fields": []
        }
    
    # Clean fields: ignore Mongo internal keys like _id
    fields = [k for k in record.keys() if not k.startswith("_")]
    
    return {
        "database": database,
        "collection": collection,
        "fields": fields
    }
# Add records to a collection
@app.tool(
    description="Insert one or more documents (records) into a given database and collection."
)
def add_record(database: str, collection: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    logger.info("INSERT DATA")
    try:
        db = client[database]
        collection_obj = db[collection]
        result = collection_obj.insert_many(records)
        cleaned_records = [clean_document(r) for r in records]

        return {
            "status": "success",
            "database": database,
            "collection": collection,
            "query": "INSERT",
            "inserted_ids": [str(_id) for _id in result.inserted_ids],
            "records": cleaned_records
        }
    except Exception as e:
        return {
            "status": "error",
            "database": database,
            "collection": collection,
            "query": "INSERT",
            "error": str(e)
        }


# Update records in a collection

@app.tool(
    description="Update one or more documents in a collection. "
                "Filter documents using `filter_field` and `filter_value`. "
                "Set a new value for `update_field` with `update_value`. "
                "Use `update_multiple_records=True` to update all matches, or False for only one."
)
def update_record(
    database: str,
    collection: str,
    filter_field: str,
    filter_value: Any,
    update_field: str,
    update_value: Any,
    update_multiple_records: bool
) -> Dict[str, Any]:
    logger.info("UPDATE DATA")
    try:
        db = client[database]
        collection_obj = db[collection]

        if update_multiple_records:
            result = collection_obj.update_many(
                {filter_field: filter_value},
                {"$set": {update_field: update_value}}
            )
        else:
            result = collection_obj.update_one(
                {filter_field: filter_value},
                {"$set": {update_field: update_value}}
            )
            print(result.matched_count)
        return {
            "status": "success",
            "database": database,
            "collection": collection,
            "query": "UPDATE",
            "matched": result.matched_count,
            "modified": result.modified_count
        }
    except Exception as e:
        return {
            "status": "error",
            "database": database,
            "collection": collection,
            "query": "UPDATE",
            "error": str(e)
        }
    

@app.tool(
    description="""
Read documents from a collection based on a MongoDB query filter.  

    🔹 **How it works:**  
    - `query_filter` is a standard MongoDB filter dictionary, e.g., `{'username': 'Aswin'}`.  
    - You can use comparison operators:  
        - `{'age': {'$gt': 25}}` → age greater than 25  
        - `{'score': {'$lte': 100}}` → score less than or equal to 100  
        - `{'status': {'$in': ['active', 'pending']}}` → match any in the list  
    - `projection` is an optional list of field names to include in the result, e.g., `['username', 'email']`.  
    - `limit` is an optional integer to limit the number of returned records.  

    ⚡ Example usage:  
    ```python
    read_records(
        database="auth-demo",
        collection="users",
        query_filter={"age": {"$gte": 18}},
        projection=["username", "age", "email"],
        limit=10
    )
    ```  

    ✅ Returns:  
    - Cleaned records with `_id` converted to string  
    - Status: `"success"` or `"error"`  
    - Count of records returned"""
)
def read_records(
    database: str,
    collection: str,
    query_filter: Optional[Dict[str, Any]] = None,
    projection: Optional[List[str]] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    logger.info("READ DATA")
    """
    Parameters:
        database (str): Database name
        collection (str): Collection name
        query_filter (dict, optional): MongoDB filter dict (e.g., {'username': 'Aswin'})
        projection (list, optional): List of fields to include in result (['_id', 'username'])
        limit (int, optional): Maximum number of records to return
    """
    try:
        db = client[database]
        collection_obj = db[collection]

        # Default to empty filter if none provided
        query_filter = query_filter or {}

        # Build projection dict if fields provided
        projection_dict = {field: 1 for field in projection} if projection else None

        cursor = collection_obj.find(query_filter, projection_dict)
        
        if limit:
            cursor = cursor.limit(limit)

        records = [clean_document(doc) for doc in cursor]
        records_json = json.loads(json.dumps(records, default=str))
        return {
            "status": "success",
            "database": database,
            "collection": collection,
            "query_filter": query_filter,
            "records": records_json,
            "count": len(records)
        }
    except Exception as e:
        return {
            "status": "error",
            "database": database,
            "collection": collection,
            "query_filter": query_filter,
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("MONGODB connected")
        app.run(transport="streamable-http", host="127.0.0.1", port=8001)
    except Exception as e:
        print(e)
