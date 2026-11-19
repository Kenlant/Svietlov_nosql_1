import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    mongo_uri: str
    db_name: str = "spotify"
    collection_name: str = "tracks_raw"
    csv_path: str = "dataset.csv"
    batch_size: int = 1000

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(mongo_uri=os.environ["MONGO_URI"])
