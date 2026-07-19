
import threading

from db.repositories.price_repository import PriceRepository


class MultiCropLoader:
    def __init__(self):
        self.repo = PriceRepository()
        self._lock = threading.Lock()
        self._results = {}

    def _fetch_one(self, crop_name: str):
        """Worker function executed inside each thread."""
        try:
            latest = self.repo.latest_for_crop(crop_name)
        except Exception:  # noqa: BLE001
            latest = None
        with self._lock:
            self._results[crop_name] = latest

    def load_many(self, crop_names: list) -> dict:
        """
        Spins up one thread per crop name, waits for all to finish (join),
        and returns {crop_name: latest_price_doc_or_None}.
        """
        self._results = {}
        threads = [threading.Thread(target=self._fetch_one, args=(name,)) for name in crop_names]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return self._results
