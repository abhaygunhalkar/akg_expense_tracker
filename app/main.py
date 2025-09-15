from fastapi import FastAPI
import yaml
import logging.config
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv()

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load logging configuration
with open("config/logging.yaml", "r") as f:
    logging_config = yaml.safe_load(f)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)
app = FastAPI()


# Import routers
from app.routes.manual_entry_routes import router as manual_entry_router
from app.routes.process_receipt_routes import router as process_receipt_router
from app.routes.search_routes import router as search_router

# Register routers
app.include_router(manual_entry_router, prefix="/api")
app.include_router(process_receipt_router, prefix="/api")
app.include_router(search_router, prefix="/api")


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the AKG Expense Tracker"}
