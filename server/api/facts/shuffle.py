from __future__ import annotations

import dataclasses
import random
from typing import ClassVar, Optional, Tuple

from api.facts.instances import ALL_FACTS
from api.facts.template import FactTemplate


def get_fact_template(shuffle_key: Optional[int]) -> Tuple[FactTemplate, int]:
    # If this key has passed through all list items, generate a new key which
    # will shuffle the list and iterate through it starting from the beginning.
    shuffle_key: ShuffleKey = ShuffleKey(shuffle_key) if shuffle_key is not None else ShuffleKey.random()
    if shuffle_key.overflow():
        shuffle_key = ShuffleKey.random()

    # Shuffle according to seed
    shuffled_templates = ALL_FACTS.copy()
    random.Random(shuffle_key.seed).shuffle(shuffled_templates)

    # Pick according to index
    fact_template = shuffled_templates[shuffle_key.index]

    # Increment shuffle key
    next_shuffle_key: int = shuffle_key.key + 1

    # Return as tuple
    return fact_template, next_shuffle_key


@dataclasses.dataclass
class ShuffleKey:
    key: int

    MAX_INDEX: ClassVar[int] = len(ALL_FACTS) - 1

    def __post_init__(self):
        # Use only first 32 bits
        self.key = self.key & 0xFFFFFFFF

    @property
    def seed(self):
        # First 24 bits
        return self.key >> 8

    @property
    def index(self):
        # Last 8 bits
        return self.key & 0xFF

    @staticmethod
    def of(seed: int, index: int) -> ShuffleKey:
        return ShuffleKey((seed << 8) & index)

    @staticmethod
    def random() -> ShuffleKey:
        random.seed()
        return ShuffleKey.of(random.getrandbits(24), 0)

    def overflow(self) -> bool:
        return self.index > ShuffleKey.MAX_INDEX
