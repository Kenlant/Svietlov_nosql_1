from spotify.application.ports import (
    Progress,
    TrackReader,
    TrackRepository,
)


class LoadTracksUseCase:
    def __init__(
        self,
        reader: TrackReader,
        repository: TrackRepository,
        progress: Progress,
        batch_size: int,
    ):
        self.reader = reader
        self.repository = repository
        self.progress = progress
        self.batch_size = batch_size

    def execute(self) -> None:
        self.repository.reset()
        dataset = self.reader.read()
        records = dataset.records
        for i in self.progress.track(range(0, len(records), self.batch_size)):
            self.repository.insert_many(records[i : i + self.batch_size])
