from dataclasses import dataclass


@dataclass(frozen=True)
class TrackDataset:
    records: list[dict]
