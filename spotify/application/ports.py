from abc import ABC, abstractmethod

from spotify.domain.track_dataset import TrackDataset


class TrackReader(ABC):
    @abstractmethod
    def read(self) -> TrackDataset: ...


class TrackRepository(ABC):
    @abstractmethod
    def reset(self) -> None: ...

    @abstractmethod
    def insert_many(self, records: list[dict]) -> None: ...


class Progress(ABC):
    @abstractmethod
    def track(self, iterable): ...
