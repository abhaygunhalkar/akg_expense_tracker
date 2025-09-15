import os
import base64
import json
from openai import AzureOpenAI
from fastapi import APIRouter, UploadFile, HTTPException
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from app.utils.utils import clean_json_string

load_dotenv()

# Initialize the FastAPI router
router = APIRouter()

AZURE_END_POINT = os.getenv("AZURE_END_POINT")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
API_VERSION = os.getenv("API_VERSION")
MODEL_NAME = os.getenv("MODEL_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

openai_client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=AZURE_END_POINT,
    api_key=SUBSCRIPTION_KEY,
)

@router.get("/funday")
async def funday():
    
    """
        A fun utility endpoint to verify LLM connectivity.

        This method is used to test that the Azure OpenAI integration is working correctly
        before invoking actual production intelligence (PI) methods. It sends a simple prompt
        to the model and returns the response, ensuring that the LLM pipeline is functional.

        Not intended for production use.
    """

    try:
        prompt_message = "Write a beautiful quote of the day."
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_message}],
            max_tokens=300,
        )
        
        print("-----------------response--------------", response)
        
        json_string = response.choices[0].message.content
        
        print("-----------------json_string--------------", json_string)
        cleaned_json_string = clean_json_string(json_string)
        
        print("-----------------cleaned_json_string--------------", cleaned_json_string)
        
        return {"message": cleaned_json_string}
    except Exception as e:
        print("-----------------error--------------", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-receipt")
async def process_receipt(file: UploadFile):
    try:
        image_bytes = await file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        prompt_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this receipt..."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[prompt_message],
            max_tokens=300,
        )

        json_string = response.choices[0].message.content
        cleaned_json_string = clean_json_string(json_string)
        expense_data: Dict[str, Any] = json.loads(cleaned_json_string)

        amount_str: Optional[str] = expense_data.get("amount")
        if amount_str is not None:
            try:
                expense_data["amount"] = float(amount_str)
            except (ValueError, TypeError):
                expense_data["amount"] = None

        return {"message": "Expense entry created successfully", "data": expense_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
