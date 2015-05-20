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
db_temp = ''


class WrongDataError(Exception):
    pass


class BaseNotFoundError(Exception):
    """
    Исключение, выбрасываемое, если запрашиваемая база не существует
    """
    pass


def add_group(group):
    """
    ДОБАВИТЬ ГРУППУ
    Принимает:
        group (str) - номер группы
    Возвращает:
        (bool) - успешность операции
    """
    if not exists(DBS_PATH):  # если нет папки с группами, создать
        mkdir(DBS_PATH)
    return True if _save_db(group, DB_STRUCTURE) else False


def add_students(group, students):
    """
    ДОБАВИТЬ СТУДЕНТОВ
    Принимает:
        group (str) - номер группы
        students (tuple) - студенты (таб. номера, имена, права)

        Пример параметра students:
        ((pers_num, name, right),
        ...
        (pers_num, name, right))

        Права необязательно указывать, по умолчанию присвоится код 0

        Коды прав пользователей:
        0 - обычный пользователь
        1 - повышенные права
        2 - суперпользователь
    Возвращает:
        (bool) - успешность операции
    """
    base = _read_db(group)
    for student in students:
        try:
            right = student[2]
        except IndexError:
            right = 0
        base['students'].update({student[0]: (student[1], right)})
    return True if _save_db(group=group, data=base) else False


def add_lessons(group, semester, lessons):
    """
    ДОБАВИТЬ СЕМЕСТР, ДАТЫ ЗАНЯТИЙ
    Принимает:
        group (str) - номер группы
        semester (str) - номер группы
        lessons (tuple) - список дат занятий
    Возвращает:
        (bool) - успешность операции
    ПРИМЕЧАНИЕ: #TODO
    """
    base = _read_db(group)
    base['semesters'].update({semester: lessons})
    return True if _save_db(group=group, data=base) else False


def update_student():
    """
    ОБНОВИТЬ ДАННЫЕ СТУДЕНТА
    """
    pass
    # TODO


def get_groups():
    """
    ПОЛУЧИТЬ СПИСОК ГРУПП
    Возвращает:
        (list) - список групп
            (str) - каждый элемент
    """
    return listdir(DBS_PATH)


def get_semesters(group):
    """
    ПОЛУЧИТЬ СПИСОК СЕМЕСТРОВ В ГРУППЕ
    Принимает:
        group (str) - номер группы
    Возвращает:
        (tuple) - список семестров
            (str) - каждый элемент
    """
    base = _read_db(group)
    return tuple(base['semesters'].keys())


def get_lessons(group, semester):
    """
    ПОЛУЧИТЬ СПИСОК ЗАНЯТИЙ (ДАТЫ) В СЕМЕСТРЕ
    Принимает:
        group (str) - номер группы
        semester (str) - номер семестра
    Возвращает:
        (tuple) - список дат занятий
    """
    base = _read_db(group)
    return base['semesters'][semester]
    # WARN: проверить работоспособность


# ВНУТРЕННИЕ ФУНКЦИИ
def _path(file):
    return DBS_PATH + '/' + file


def _read_db(group):
    global db_temp
    path = _path(group)
    if not exists(path):
        raise BaseNotFoundError
    base = open(path, 'r').read()
    db_temp = base
    return json.loads(base)


def _save_db(group, data):
    path = _path(group)
    try:
        with open(path, 'w') as file:
            file.write(json.dumps(data))
            file.close()
    except ValueError:
        with open(path, 'w') as base:
            base.write(db_temp)
            base.close()
    return True
