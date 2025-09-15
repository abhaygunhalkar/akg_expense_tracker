from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pymongo.errors import ConnectionFailure, OperationFailure

from app.db.database import db_client, test_connection, collection

# Initialize the FastAPI router
router = APIRouter()

@router.get("/search")
async def search_entries(
    category: Optional[str] = None,
    amount: Optional[float] = None,
    date: Optional[str] = None,
    description: Optional[str] = None,
) -> List[Dict[str, Any]]:
    try:
        print("Beforfe Test connection------------------!")
        if test_connection():
            print("MongoDB connection test passed!")
            print("Successfully connected to Azure Cosmos DB.")
        else:
            raise ConnectionFailure("Failed to connect to the database after test.")

        all_records = list(collection.find({}))

        for record in all_records:
            record["_id"] = str(record["_id"])

        filtered_records = []
        for record in all_records:
            if category and record.get("category") != category:
                continue
            if amount and record.get("amount") != amount:
                continue
            if date and record.get("date") != date:
                continue
            if (
                description
                and record.get("description")
                and description.lower() not in record["description"].lower()
            ):
                continue

            filtered_records.append(record)

        return filtered_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
