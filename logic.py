# coding: utf-8
import json
from os.path import exists  # проверка существования файла
from os import mkdir, listdir
from pprint import pprint  # TEMP

DBS_PATH = 'groups'
DB_STRUCTURE = \
    {
        'students': {},
        'attendance': {}
    }
db_temp = ''


class BaseNotFoundError(Exception):
    """
    Исключение, выбрасываемое, если запрашиваемая база не существует
    """
    pass


def add(group, semester='', subject=''):
    """
    ДОБАВИТЬ ГРУППУ И/ИЛИ СЕМЕСТР
    Принимает:
        group (str или int) - номер группы
        semester (str или int), необязательный - номер группы
    Возвращает:
        (bool) - успешность операции
    """
    group = str(group)
    semester = str(semester)
    if not exists(DBS_PATH):  # если нет папки с группами, создать
        mkdir(DBS_PATH)
    path = DBS_PATH + '/' + group
    if not exists(path):
        mkdir(path)
    elif not semester:
        return False
    if semester:
        path += '/' + semester
        if not exists(path):
            mkdir(path)
        elif not subject:
            return False
    if subject:
        path +=  '/' + subject
        with open(path, 'w') as file:
            file.write(json.dumps(DB_STRUCTURE))
    return True
    # FIXME: оптимизировать код


def get_groups():
    """
    ПОЛУЧИТЬ СПИСОК ГРУПП
    Возвращает:
        (list) - список групп
            (str) - каждый элемент
    """
    if not exists(DBS_PATH):
        mkdir(DBS_PATH)
        return ()
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
    return listdir(DBS_PATH + '/' + group)


class Subject:
    """
    Принимает:
            group (str) или (int) - номер группы
            semester (str) или (int) - номер группы
            subject (str) - название предмета
    """
    def __init__(self, group, semester, subject):
        self.group = str(group)
        self.semester = str(semester)
        self.subject = subject
        self.path = self._path()
        if not exists(self.path):
            raise BaseNotFoundError('База данных \"%s\" не найдена' % self.path)
        self.base = self._read_db()

    def add_students(self, students):
        """
        ДОБАВИТЬ СТУДЕНТОВ
        Принимает:
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
        for student in students:
            try:
                right = student[2]
            except IndexError:
                right = 0
            self.base['students'].update({student[0]: (student[1], right)})
        # TODO: заполнить посещаемость нулями
        return True if self._save_db() else False

    def add_lessons(self, lessons):
        """
        ДОБАВИТЬ СЕМЕСТР, ДАТЫ ЗАНЯТИЙ
        Принимает:
            lessons (tuple) - список дат занятий
        Возвращает:
            (bool) - успешность операции
        ПРИМЕЧАНИЕ: #TODO
        """

        for lesson in lessons:
            self.base['attendance'].update({lesson: {}})
        # TODO: заполнить посещаемость нулями
        return True if self._save_db() else False

    def update_student(self):
        """
        ОБНОВИТЬ ДАННЫЕ СТУДЕНТА
        """
        pass
        # TODO

    def check_in(self, date, pers_number, code=1):
        """
        ОТМЕТИТЬСЯ
        Принимает:
            date (str) - дата занятия
            pers_number (str или int)  - табельный номер
            code (str или int) - код посещения
                0 - не посещал
                1 - без опоздания (по умолчанию)
                2 - опоздание небольшое
                3 - большое
        """
        pers_number = str(pers_number)
        code = str(code)
        if pers_number in self.base['students'] and date in self.base['attendance']:
            self.base['attendance'][date].update({pers_number: code})
            return True if self._save_db() else False
        else:
            return False

    def get_student_info(self, pers_number='', name=''):
        """
        ПОЛУЧИТЬ ИНФОРМАЦИЮ О СТУДЕНТЕ
        """
        pass
        # TODO

    def get_names(self):
        """
        ПОЛУЧИТЬ СПИСОК СТУДЕНТОВ
        Принимает:
            group (str) - номер группы
        Возвращает:
            (tuple) - список из имён студентов
        """
        return tuple(self.base['students'][student][0] for student in self.base['students'])

    def get_lessons(self):
        """
        ПОЛУЧИТЬ СПИСОК ЗАНЯТИЙ (ДАТЫ) В СЕМЕСТРЕ
        Принимает:
            group (str) - номер группы
            semester (str) - номер семестра
        Возвращает:
            (tuple) - список дат занятий
        """
        return tuple(self.base['attendance'].keys())

    def get_values_semester(self):
        """
        ПОЛУЧИТЬ ДАННЫЕ ПО СЕМЕСТРУ (ИМЕНА, ДАТЫ, КОДЫ ПОСЕЩЕНИЙ)
        Принимает:
            group (str) - номер группы
            semester (str) - номер семестра
        Возвращает:
            (dist)

        ПРИМЕР:
            # TODO
        """
        students = {student: self.base['students'][student][0] for student in self.base['students']}
        value = {}
        for date in self.base['attendance']:
            for student in self.base['attendance'][date]:
                value.update({date: {students[student]: self.base['attendance'][date][student]}})
        return value
        # WARN: проверить работоспособность
        # REVIEW: посмотреть, нельзя ли переписать

    def del_semester(self):
        pass
        # TODO

    def del_student(self):
        pass
        # TODO

    def del_lessons(self):
        pass
        # TODO

    # ВНУТРЕННИЕ ФУНКЦИИ
    def _path(self):
        return DBS_PATH + '/' + self.group + '/' + self.semester + '/' + self.subject

    def _read_db(self):
        global db_temp
        base = open(self.path, 'r').read()
        db_temp = base  # создание резервной копии базы в памяти
        return json.loads(base)

    def _save_db(self):
        try:
            with open(self.path, 'w') as file:
                file.write(json.dumps(self.base))
        except ValueError:  # в случае возникновения ошибки, записать в файл первоначальный вид базы
            with open(self.path, 'w') as base:
                base.write(db_temp)
                return False
        return True
