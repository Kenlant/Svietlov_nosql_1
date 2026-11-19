import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pymongo import MongoClient

from spotify.application.load_tracks import LoadTracksUseCase
from spotify.infrastructure.mongo_track_repository import MongoTrackRepository
from spotify.infrastructure.pandas_track_reader import PandasTrackReader
from spotify.infrastructure.settings import Settings
from spotify.infrastructure.tqdm_progress import TqdmProgress


def main() -> None:
    settings = Settings.from_env()
    client = MongoClient(settings.mongo_uri)
    collection = client[settings.db_name][settings.collection_name]
    LoadTracksUseCase(
        PandasTrackReader(settings.csv_path),
        MongoTrackRepository(collection),
        TqdmProgress(),
        settings.batch_size,
    ).execute()


if __name__ == "__main__":
    main()
