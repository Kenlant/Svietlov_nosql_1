from pymongo.collection import Collection

from spotify.application.ports import TrackRepository


class MongoTrackRepository(TrackRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    def reset(self) -> None:
        self.collection.drop()

    def insert_many(self, records: list[dict]) -> None:
        self.collection.insert_many(records)
