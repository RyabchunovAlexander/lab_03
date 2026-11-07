class CatalogError(Exception):
    """Базовое исключение для всех ошибок каталога."""


class InvalidItemError(CatalogError):
    """Неверная сущность"""


class DuplicateIdError(CatalogError):
    """Дубликат ID"""


class NotFoundError(CatalogError):
    """Объект не найден"""


class FormatError(CatalogError):
    """Неподдерживаемая версия формата"""


class CorruptedFileError(CatalogError):
    """Повреждённый файл"""