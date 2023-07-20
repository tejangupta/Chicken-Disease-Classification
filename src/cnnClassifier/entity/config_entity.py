from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    region: str
    bucket: str
    path: str
    local_data_file: Path
    unzip_dir: Path
    aws_access_key: str
    aws_secret_key: str
