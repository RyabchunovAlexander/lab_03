from .errors import DuplicateIdError, NotFoundError


class Catalog:
    """Класс для управления коллекцией медиафайлов."""

    def __init__(self):
        """Создаёт пустой каталог и индекс по категориям."""
        self._items = {}
        self._by_category = {}

    @property
    def view(self):
        """Возвращает read-only представление каталога (копию)."""
        return dict(self._items)

    def add(self, item):
        """Добавляет медиафайл в каталог."""
        if item.item_id in self._items:
            raise DuplicateIdError(f"Медиафайл с ID {item.item_id} уже есть")

        self._items[item.item_id] = item

        cat_name = item.category.lower()
        if cat_name not in self._by_category:
            self._by_category[cat_name] = []
        self._by_category[cat_name].append(item)

    def get(self, item_id):
        """Возвращает медиафайл по его ID."""
        if item_id not in self._items:
            raise NotFoundError(f'Медиафайл с ID {item_id} не найден')
        return self._items[item_id]

    def remove(self, item_id):
        """Удаляет медиафайл по его ID."""
        if item_id not in self._items:
            raise NotFoundError(f'Медиафайл с ID {item_id} не найден')

        item = self._items[item_id]

        cat_name = item.category.lower()
        self._by_category[cat_name].remove(item)
        if not self._by_category[cat_name]:
            del self._by_category[cat_name]

        del self._items[item_id]

    def find_by_category(self, category):
        """Ищет все медиафайлы определенной категории (по индексу)."""
        cat_name = category.lower()
        if cat_name not in self._by_category:
            return []
        return list(self._by_category[cat_name])

    def find_by_name(self, query):
        """Ищет медиафайлы, в названии которых есть подстрока."""
        res = []
        for item in self._items.values():
            if query.lower() in item.title.lower():
                res.append(item)
        return res

    def __len__(self):
        """Возвращает количество медиафайлов в каталоге."""
        return len(self._items)

    def __iter__(self):
        """Позволяет перебирать медиафайлы в порядке возрастания ID."""
        keys = sorted(self._items.keys())
        for k in keys:
            yield self._items[k]

    def __contains__(self, item_id):
        """Позволяет проверять наличие ID в каталоге."""
        return item_id in self._items
