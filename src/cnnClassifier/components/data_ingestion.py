import os
import zipfile
import boto3
from src.cnnClassifier import logger
from src.cnnClassifier.utils.utils import get_size
from src.cnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.s3_client = boto3.client(
            's3',
            region_name=self.config.region,
            aws_access_key_id=self.config.aws_access_key,
            aws_secret_access_key=self.config.aws_secret_key
        )
    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            logger.info(f"Downloading {self.config.path} from {self.config.bucket}...")
            self.s3_client.download_file(self.config.bucket, self.config.path, str(self.config.local_data_file))
            logger.info(f"Download complete: {self.config.local_data_file}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
