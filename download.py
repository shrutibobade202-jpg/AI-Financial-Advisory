from huggingface_hub import snapshot_download
from huggingface_hub import login
from utils.central_logging import setup_logging,get_logger
import os

#setup_logging()
logger = get_logger("hugging-face")
# Get our API keys
hf_token = os.getenv("HF_TOKEN")

if hf_token:
    logger.info("Hugging face token has been set")
else:
    logger.info("Error no hugging face token found")

# Loggin to huggingface
try:
    login(hf_token)
    logger.info("Logging to Hugging face has been successful")
except Exception as e:
    logger.exception(f"An error occurred when loging to Hugging face: {e}")



def dowload_vectorial_db():
    repo_id = "Cedric07/financial-vector-db"
    local_download_path = snapshot_download(
        repo_id=repo_id,
        repo_type="dataset",
        local_dir = '',
        local_dir_use_symlinks=False,
    )
    logger.info(f"Downloaded to: {local_download_path}")