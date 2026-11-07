from .catalog import Catalog
from .errors import InvalidItemError
from .models import MediaItem
from .storage import save, load

def main():
    """Запускает демонстрационный сценарий."""
    m1 = MediaItem('1', 'Ирония судьбы', 'Фильм', 1975, 'Эльдар Рязанов', 184)
    m2 = MediaItem('2', 'Группа крови', 'Музыка', 1988, 'Кино', 47)

    print('Создано:', m1.title, 'и', m2.title)

    try:
        MediaItem('3', 'Без времени', 'Фильм', 2020, 'Неизвестен', 0)
    except InvalidItemError as e:
        print('Ошибка при создании:', e)

    cat = Catalog()
    cat.add(m1)
    cat.add(m2)

    print('Всего в каталоге:', len(cat))
    print('Поиск фильмов:', len(cat.find_by_category('фильм')))

    save(cat, 'data.json')
    print('Сохранено в файл data.json')

    new_cat = Catalog()
    load(new_cat, 'data.json')
    print('Загружено из файла:', len(new_cat))

if __name__ == '__main__':
    main()