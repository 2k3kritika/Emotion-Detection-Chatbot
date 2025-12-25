import pickle
from typing import List, Dict, Any


class LabelEncoderWrapper:
    """A tiny label encoder with save/load that does not require sklearn.

    - fit(labels): builds mapping
    - transform(labels): returns list[int]
    - inverse_transform(indices): returns list[str]
    - save(path) / load(path)
    """

    def __init__(self) -> None:
        self.class_to_index: Dict[str, int] = {}
        self.index_to_class: Dict[int, str] = {}

    def fit(self, labels: List[str]) -> None:
        uniques = sorted(set(labels))
        self.class_to_index = {c: i for i, c in enumerate(uniques)}
        self.index_to_class = {i: c for c, i in self.class_to_index.items()}

    def transform(self, labels: List[str]) -> List[int]:
        return [self.class_to_index.get(l, -1) for l in labels]

    def inverse_transform(self, indices: List[int]) -> List[str]:
        return [self.index_to_class.get(i, None) for i in indices]

    def save(self, filepath: str) -> None:
        with open(filepath, "wb") as f:
            pickle.dump({"class_to_index": self.class_to_index, "index_to_class": self.index_to_class}, f)

    @classmethod
    def load(cls, filepath: str) -> "LabelEncoderWrapper":
        inst = cls()
        with open(filepath, "rb") as f:
            data: Any = pickle.load(f)
        inst.class_to_index = data.get("class_to_index", {})
        inst.index_to_class = data.get("index_to_class", {})
        return inst
