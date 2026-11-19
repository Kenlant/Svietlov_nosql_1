from tqdm import tqdm

from spotify.application.ports import Progress


class TqdmProgress(Progress):
    def track(self, iterable):
        return tqdm(iterable)
