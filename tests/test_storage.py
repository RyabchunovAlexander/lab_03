import pytest

from catalog.catalog import Catalog
from catalog.errors import CorruptedFileError, FormatError
from catalog.models import MediaItem
from catalog.storage import load, save


def test_save_load(tmp_path):
    """Проверка сохранения и загрузки каталога."""
    file = tmp_path / 'data.json'
    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))

    save(cat, file)

    new_cat = Catalog()
    load(new_cat, file)

    assert len(new_cat) == 1
    assert new_cat.get('1').title == 'Ирония судьбы'


def test_unicode_saved(tmp_path):
    """Проверка, что кириллица сохраняется в файл."""
    file = tmp_path / 'data.json'
    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))

    save(cat, file)

    text = file.read_text(encoding='utf-8')
    assert 'Ирония' in text
    assert '\\u' not in text


def test_missing_file(tmp_path):
    """Проверка, что загрузка несуществующего файла вызывает ошибку."""
    file = tmp_path / 'no_file.json'

    with pytest.raises(CorruptedFileError):
        load(Catalog(), file)


def test_bad_version(tmp_path):
    """Проверка, что файл с неверной версией формата отклоняется."""
    file = tmp_path / 'data.json'
    file.write_text('{"format_version": 999, "items": []}')

    with pytest.raises(FormatError):
        load(Catalog(), file)


def test_corrupted_json(tmp_path):
    """Проверка, что битый JSON вызывает ошибку."""
    file = tmp_path / 'data.json'
    file.write_text('это не json')

    with pytest.raises(CorruptedFileError):
        load(Catalog(), file)


def test_atomicity(tmp_path):
    """Проверка, что при ошибке загрузки старый каталог не меняется."""
    file = tmp_path / 'data.json'
    file.write_text('{"format_version": 1, "items": [{"item_id": "2"}]}')

    cat = Catalog()
    cat.add(MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184))

    with pytest.raises(CorruptedFileError):
        load(cat, file)

    assert len(cat) == 1
    assert '1' in cat
    assert cat.get('1').title == 'Ирония судьбы'