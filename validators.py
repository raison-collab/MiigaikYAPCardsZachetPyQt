import typing


class FieldValidator:
    def valid_fields(self) -> bool:
        ...

    def clear_fields(self):
        ...

    def count_words(self, st: str) -> int:
        return len(st.split())

    def is_empty(self, st: str) -> bool:
        return not bool(len(st))
