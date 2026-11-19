import pandas as pd

from spotify.application.ports import TrackReader
from spotify.domain.track_dataset import TrackDataset
from spotify.domain.track_schema import TrackSchema


class PandasTrackReader(TrackReader):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def read(self) -> TrackDataset:
        df = pd.read_csv(self.csv_path)
        for col in TrackSchema.BOOL_COLUMNS:
            df[col] = df[col].astype(bool)
        for col in TrackSchema.INT_COLUMNS:
            df[col] = df[col].astype(int)
        for col in TrackSchema.FLOAT_COLUMNS:
            df[col] = df[col].astype(float)
        missing = df[list(TrackSchema.REQUIRED_COLUMNS)].isna().any(axis=1)
        records = df[~missing].to_dict("records")
        return TrackDataset(records)
