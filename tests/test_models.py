import pytest

from catalog.errors import InvalidItemError
from catalog.models import MediaItem


def test_create_movie():
    """Проверка успешного создания корректного фильма."""
    item = MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184)
    assert item.item_id == '1'
    assert item.title == 'Ирония судьбы'
    assert item.category == 'Фильм'
    assert item.duration == 184


def test_create_music():
    """Проверка создания музыкального трека."""
    item = MediaItem('2', 'Группа крови', 'Музыка', 1988, 'Кино', 4)
    assert item.title == 'Группа крови'
    assert item.category == 'Музыка'
    assert item.duration == 4


def test_year():
    """Проверка, что медиафайл нынешнего года не вызывает ошибку"""
    item = MediaItem('3', 'Буратино', 'Фильм', 2026, 'Игорь Волошин', 102)
    assert item.year == 2026


def test_empty_id():
    """Пустой ID должен вызывать ошибку."""
    with pytest.raises(InvalidItemError):
        MediaItem('', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184)


def test_empty_title():
    """Пустое название должно вызывать ошибку."""
    with pytest.raises(InvalidItemError):
        MediaItem('1', '', 'Фильм', 1975, 'Эльдар Рязанов', 184)


def test_empty_category():
    """Пустой автор должен вызывать ошибку."""
    with pytest.raises(InvalidItemError):
        MediaItem('1', 'Ирония судьбы', '', 1975, 'Эльдар Рязанов', 184)


def test_empty_author():
    """Пустой автор должен вызывать ошибку."""
    with pytest.raises(InvalidItemError):
        MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, '', 184)


def test_incorrect_year():
    """Год выпуска не может быть из будущуго."""
    with pytest.raises(InvalidItemError):
        MediaItem('1', 'Ирония судьбы', 'Фильм', 2100, 'Эльдар Рязанов', 184)


def test_incorrect_duration():
    """Длительность не ожет быть отрицательной."""
    with pytest.raises(InvalidItemError):
        MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', -184)