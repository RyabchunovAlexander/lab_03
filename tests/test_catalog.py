import pytest

from catalog.catalog import Catalog
from catalog.errors import DuplicateIdError, NotFoundError
from catalog.models import MediaItem


def test_empty_catalog():
    """Проверка, что новый каталог пуст."""
    cat = Catalog()
    assert len(cat) == 0
    assert list(cat) == []
    assert '1' not in cat


def test_add_get_remove():
    """Проверка добавления, получения и удаления элемента."""
    cat = Catalog()
    item = MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184)

    cat.add(item)
    assert len(cat) == 1
    assert '1' in cat
    assert cat.get('1') == item

    cat.remove('1')
    assert len(cat) == 0
    assert '1' not in cat


def test_duplicate_id():
    """Проверка добавления элемента с существующим ID."""
    cat = Catalog()
    item = MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184)
    cat.add(item)

    with pytest.raises(DuplicateIdError):
        cat.add(item)


def test_not_found():
    """Проверка удаления или получения несуществующего ID."""
    cat = Catalog()

    with pytest.raises(NotFoundError):
        cat.get('999')
    with pytest.raises(NotFoundError):
        cat.remove('999')


def test_find_by_category():
    """Проверка поиска по категории без учёта регистра."""
    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))
    cat.add(MediaItem('2', 'Служебный роман', 'Фильм', 1977, 'Эльдар Рязанов', 159))
    cat.add(MediaItem('3', 'Группа крови', 'Музыка', 1988, 'Кино', 4))

    found = cat.find_by_category('фильм')
    assert len(found) == 2


def test_find_by_name():
    """Проверка поиска по названию без учёта регистра."""
    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))
    cat.add(MediaItem('2', 'Служебный роман', 'Фильм', 1977, 'Эльдар Рязанов', 159))

    found = cat.find_by_name('ИРОНИЯ')
    assert len(found) == 1


def test_find_returns_new_list():
    """Проверка, что поиск возвращает копию, а не внутренний список."""
    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))

    found = cat.find_by_category('фильм')
    found.clear()

    assert len(cat) == 1


def test_iteration_order():
    """Проверка, что итерация идёт в отсортированном порядке (по ID"""
    cat = Catalog()
    cat.add(MediaItem('3', 'Группа крови', 'Музыка', 1988, 'Кино', 4))
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))
    cat.add(MediaItem('2', 'Служебный роман', 'Фильм', 1977, 'Эльдар Рязанов', 159))

    item_ids = [item.item_id for item in cat]
    assert item_ids == ['1', '2', '3']


def test_read_only_view():
    """Проверка, что представление защищено от изменений."""
    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))

    view = cat.view
    del view['1']

    assert len(cat) == 1
    assert '1' in cat


def test_category_index():
    """Проверка, что индекс категорий обновляется при добавлении и удалении."""
    cat = Catalog()

    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))
    cat.add(MediaItem('2', 'Служебный роман', 'Фильм', 1977, 'Эльдар Рязанов', 159))
    cat.add(MediaItem('3', 'Группа крови', 'Музыка', 1988, 'Кино', 4))

    assert len(cat.find_by_category('фильм')) == 2
    assert len(cat.find_by_category('музыка')) == 1

    cat.remove('1')

    assert len(cat.find_by_category('фильм')) == 1
    assert cat.find_by_category('фильм')[0].item_id == '2'

    cat.remove('3')
    assert len(cat.find_by_category('музыка')) == 0