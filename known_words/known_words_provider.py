from abc import ABC, abstractmethod
from typing import Set

class KnownWordsProvider(ABC):
    @abstractmethod
    def get_known_words(self) -> Set[str]:
        """Return a set of known words (as kanji/kana strings)."""
        pass
