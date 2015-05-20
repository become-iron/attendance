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
    base = _decode_db(group)
    for student in students:
        try:
            right = student[2]
        except IndexError:
            right = 0
        base['students'].update({student[0]: (student[1], right)})
    return True if _save_db(group=group, data=base) else False


def get_groups():
    """
    ПОЛУЧИТЬ СПИСОК ГРУПП
    Возвращает:
        (list) - список групп
            (str) - каждый элемент
    """
    # return tuple(map(lambda x: x.replace('.db', ''), listdir(DBS_PATH)))
    return listdir(DBS_PATH)


def get_semesters(group):
    """
    ПОЛУЧИТЬ СПИСОК СЕМЕСТРОВ В ГРУППЕ
    Принимает:
        (str) или (int) - номер группы
    Возвращает:
        (tuple) - список семестров
            (str) - каждый элемент
    """
    base = _decode_db(group)
    return tuple(base['semesters'].keys())


def _decode_db(group):
    if isinstance(group, str) or isinstance(group, int):
        group = str(group)
    else:
        raise WrongDataError('Параметр group должен быть int или str')
    path = _path(group)
    if not exists(path):
        raise BaseNotFoundError
    base = open(path, 'r').read()
    return json.loads(base)


def _save_db(group, data):
    if isinstance(group, str) or isinstance(group, int):
        group = str(group)
    else:
        raise WrongDataError('Параметр group должен быть int или str')
    path = _path(group)
    with open(path, 'w') as file:
        file.write(json.dumps(data))
        file.close()
    return True


def _path(file):
    return DBS_PATH + '/' + file
