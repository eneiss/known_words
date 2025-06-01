import requests
import json
import os
import time

from typing import Set

from known_words_provider import KnownWordsProvider

# Self rate-limiting
def sleep(duration=0.5):
    print(f"sleeping for {duration}")
    time.sleep(duration)

class WanikaniKnownWordsProvider(KnownWordsProvider):
    def __init__(self, api_key: str, cache_path="../output/wanikani_known_words.json"):
        self.api_key = api_key
        self.cache_path = cache_path

    def get_known_words(self, use_cache=True) -> Set[str]:
        # Read from cache first
        if use_cache and os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return set(json.load(f))

        return self._import_wk_known_words()

    def _import_wk_known_words(self) -> Set[str]:
        known_item_ids = []
        headers = {"Authorization": f"Bearer {self.api_key}", "Wanikani-Revision": "20170710"}
        # TODO: filter by SRS level/WK level
        url = "https://api.wanikani.com/v2/assignments?subject_types=vocabulary&started=true"
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            for item in data["data"]:
                known_item_ids.append(item["data"]["subject_id"])
            url = data["pages"]["next_url"]

            sleep()

        # Resolve subject_ids to actual vocab using a separate request
        known_vocab = self._resolve_vocab_meanings(known_item_ids, headers)

        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(list(known_vocab), f, ensure_ascii=False)

        return known_vocab

    def _resolve_vocab_meanings(self, subject_ids, headers):
        known_vocab = set()
        for chunk in self._chunked(subject_ids, 1000):
            url = f"https://api.wanikani.com/v2/subjects?ids={','.join(map(str, chunk))}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            for item in data["data"]:
                if item["object"] == "vocabulary":
                    known_vocab.add(item["data"]["characters"])
            sleep()
        return known_vocab

    def _chunked(self, iterable, size):
        for i in range(0, len(iterable), size):
            yield iterable[i:i + size]  # Does not work on sets
