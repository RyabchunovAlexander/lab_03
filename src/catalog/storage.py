import json
from .errors import CorruptedFileError, FormatError
from .models import MediaItem

def save(catalog, filename):
    """Сохраняет каталог в JSON-файл."""
    items_list = []
    for item in catalog:
        info = {
            'item_id': item.item.id,
            'title': item.title,
            'category': item.category,
            'year': item.year,
            'author': item.author,
            'duration': item.duration
        }
        items_list.append(info)

    data = {
        'format_version': 1,
        'items': items_list
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def load(catalog, filename):
    """Загружает каталог из JSON-файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        raise CorruptedFileError('Не удалось прочитать файл или он повреждён')

    if data.get('format_version') != 1:
        raise FormatError('Неподдерживаемая версия формата')

    new_items = {}
    try:
        for raw in data['items']:
            item = MediaItem(
                item_id=raw['item_id'],
                title=raw['title'],
                category=raw['category'],
                year=raw['year'],
                author=raw['author'],
                duration=raw['duration']
            )
            if item.item_id in new_items:
                raise CorruptedFileError('Дубликат ID в файле')
            new_items[item.item_id] = item
    except (KeyError, TypeError):
        raise CorruptedFileError('В файле не хватает данных')

    catalog._items = new_items