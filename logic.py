# coding: utf-8
import json
from os.path import exists  # проверка существования файла
from os import mkdir, listdir

DBS_PATH = 'groups'
DB_STRUCTURE = \
    {
        'students': {},
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
    for lesson in lessons:
        base['attendance'][semester].update({lesson: {}})
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


def get_students(group):
    """
    ПОЛУЧИТЬ СПИСОК СТУДЕНТОВ
    Принимает:
        group (str) - номер группы
    Возвращает:
        (tuple) - список из имён студентов
    """
    base = _read_db(group)
    return tuple(base['students'][student][0] for student in base['students'])


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
    return tuple(semester for semester in base['attendance'])


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
    return tuple(date for date in base['attendance'][semester])


def get_values_semester(group, semester):
    """
    ПОЛУЧИТЬ ДАННЫЕ ПО СЕМЕСТРУ
    Принимает:
        group (str) - номер группы
        semester (str) - номер семестра
    Возвращает:
        (dist)

    ПРИМЕР:
        # TODO
    """
    base = _read_db(group)
    students = {student: base['students'][student][0] for student in base['students']}
    value = {}
    for date in base['attendance'][semester]:
        for student in base['attendance'][semester][date]:
            value.update({date: {students[student]: base['attendance'][semester][date][student]}})
    return value
    # WARN: проверить работоспособность


def check_in(group, semester, date, pers_number, code=1):
    """
    ОТМЕТИТЬСЯ
    Принимает:
        group (str) - номер группы
        semester (str) - номер семестра
        date (str) - дата занятия
        pers_number (str) - табельный номер
        code (str) - код посещения
            0 - не посещал
            1 - без опоздания (по молчанию)
            2 - опоздание небольшое
            3 - большое
    """
    base = _read_db(group)
    if pers_number in base['students']:
        base['attendance'][semester][date].update({pers_number: code})
        return True if _save_db(group, base) else False
    else:
        return False


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
            return False
    return True
