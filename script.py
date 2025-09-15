import os

project_name = "."
folders = [
    f"{project_name}/app/routes",
    f"{project_name}/app/models",
    f"{project_name}/app/services",
    f"{project_name}/app/utils",
    f"{project_name}/app/db",
    f"{project_name}/config",
    f"{project_name}/logs",
    f"{project_name}/tests"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# pyproject.toml
pyproject_content = """[project]
name = "akg_expense_tracker"
version = "0.1.0"
description = "A production-level API project"
authors = [{name = "Your Name", email = "your.email@example.com"}]
dependencies = ["fastapi", "uvicorn", "pydantic", "pyyaml", "python-dotenv"]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
"""
with open(f"{project_name}/pyproject.toml", "w") as f:
    f.write(pyproject_content)

# requirements.txt
requirements_content = """fastapi
uvicorn
pydantic
pyyaml
python-dotenv
"""
with open(f"{project_name}/requirements.txt", "w") as f:
    f.write(requirements_content)

# .env
env_content = """APP_NAME=akg_expense_tracker
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=INFO
"""
with open(f"{project_name}/.env", "w") as f:
    f.write(env_content)

# config.yaml
config_yaml_content = """app:
  name: akg_expense_tracker
  host: 127.0.0.1
  port: 8000

logging:
  level: INFO
  file: logs/app.log
"""
with open(f"{project_name}/config/config.yaml", "w") as f:
    f.write(config_yaml_content)

# logging.yaml
logging_yaml_content = """version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  file:
    class: logging.FileHandler
    filename: logs/app.log
    formatter: simple
    level: INFO
root:
  handlers: [file]
  level: INFO
"""
with open(f"{project_name}/config/logging.yaml", "w") as f:
    f.write(logging_yaml_content)

# main.py
main_py_content = """from fastapi import FastAPI
import yaml
import logging.config
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load logging configuration
with open("config/logging.yaml", "r") as f:
    logging_config = yaml.safe_load(f)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the API project"}
"""
with open(f"{project_name}/app/main.py", "w") as f:
    f.write(main_py_content)

print(f"Production-level API project structure created in '{project_name}' directory.")
