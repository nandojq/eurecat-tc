
# Importing
import logging
import os

from ingestion.ingestion import trigger_ingestion
from processing.dataProcessing import process_data

# Setup logger
logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

# Mock pipeline process
try:
    ingest_data = trigger_ingestion()
    process_data(ingest_data)
    logger.info("Successful run")
except Exception as e:
    logger.error(e)
