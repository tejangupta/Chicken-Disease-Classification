from src.cnnClassifier.constants import *
from src.cnnClassifier.utils.utils import read_yaml, create_directories
from src.cnnClassifier.entity.config_entity import DataIngestionConfig


class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        secrets_filepath=SECRETS_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.secrets = read_yaml(secrets_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        secrets = self.secrets.s3
        credentials = self.secrets.aws_credentials

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            region=secrets.region,
            bucket=secrets.bucket,
            path=secrets.path,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            aws_access_key=credentials.access_key,
            aws_secret_key=credentials.secret_key
        )

        return data_ingestion_config
