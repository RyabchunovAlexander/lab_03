from dataclasses import dataclass
from .errors import InvalidItemError

@dataclass
class MediaItem:
    item_id: str
    title: str
    category: str
    year: int
    author: str
    duration: int

    def __post_init__(self):
        if not isinstance(self.item_id, str):
            raise InvalidItemError('ID должен быть строкой')
        if not self.item_id.strip():
            raise InvalidItemError('ID не может быть пустым')

        if not isinstance(self.title, str):
            raise InvalidItemError('Название должно быть строкой')
        if not self.title.strip():
            raise InvalidItemError('Название не может быть пустым')

        if not isinstance(self.category, str):
            raise InvalidItemError('Категория должна быть строкой')
        if not self.category.strip():
            raise InvalidItemError('Категория не может быть пустой')

        if not isinstance(self.year, int):
            raise InvalidItemError('Год должен быть числом')
        if self.year > 2026:
            raise InvalidItemError('Некорректный год')

        if not isinstance(self.author, str):
            raise InvalidItemError('Автор должен быть строкой')
        if not self.author.strip():
            raise InvalidItemError('Автор не может быть пустым')

        if not isinstance(self.duration, int):
            raise InvalidItemError('Длительность должна быть числом')
        if self.duration <= 0:
            raise InvalidItemError('Длительность должна быть больше нуля')