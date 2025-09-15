from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.db.database import collection

# Initialize the FastAPI router
router = APIRouter()

class ExpenseEntry(BaseModel):
    amount: float
    category: str
    date: str
    description: str


@router.post("/manual-entry")
async def manual_entry(entry: ExpenseEntry):
    try:
        entry_data = entry.dict()
        result = collection.insert_one(entry_data)
        entry_data.pop("_id", None)
        return {"message": "Manual entry created successfully", "data": entry_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
