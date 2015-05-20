# coding: utf-8
import json
from os.path import exists  # проверка существования файла
from os import mkdir, listdir

DBS_PATH = 'groups'
DB_STRUCTURE = \
    {
        'students': {},
        'semesters': {},
        'attendance': {}
    }


class WrongDataError(Exception):
    pass


class BaseNotFoundError(Exception):
    """
    Исключение, выбрасываемое, если запрашиваемая база не существует
    """
    pass


def add_group(group):
    if isinstance(group, str) or isinstance(group, int):
        group = str(group)
    else:
        raise WrongDataError('Параметр group должен быть int или str')
    # если нет папки с группами, создать
    if not exists(DBS_PATH):
        mkdir(DBS_PATH)
    # создать пустой файл для группы
    path = DBS_PATH + '/' + group
    if exists(path):
        return False
    with open(path, 'w') as db:
        # записать в файл основную структуру базы
        _ = json.dumps(DB_STRUCTURE)
        db.write(_)
        db.close()
    return True


def add_students(group, students):
    """
    ((pers_num, name, right),
    ...
    (pers_num, name, right))
    """
    if isinstance(group, str) or isinstance(group, int):
        group = str(group)
    else:
        raise WrongDataError('Параметр group должен быть int или str')
    path = _path(group)
    base = _decode_db(path)
    print(base)
    for student in students:
        try:
            right = student[2]
        except IndexError:
            right = 0
        base['students'].update({student[0]: (student[1], right)})
    print(base)
    return True if _save_db(path=path, data=base) else False


def get_list_of_groups():
    """
    ПОЛУЧИТЬ СПИСОК ГРУПП
    Возвращает:
        (tuple) - список групп
            (str) - каждый элемент
        Пример: ('2342', '3244, 'и3242')
    """
    # return tuple(map(lambda x: x.replace('.db', ''), listdir(DBS_PATH)))
    return listdir(DBS_PATH)


def _decode_db(path):
    if not exists(path):
        raise BaseNotFoundError
    _ = open(path, 'r').read()
    return json.loads(_)


def _save_db(path, data):
    print(data)
    with open(path, 'w') as file:
        file.write(json.dumps(data))
        file.close()
    return True


def _path(file):
    return DBS_PATH + '/' + file
