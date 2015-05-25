# coding: utf-8
import json
from os.path import exists  # проверка существования файла
from os import mkdir, listdir
import logging
from pprint import pprint  # TEMP

logging.basicConfig(format = '%(levelname)-7s:(line %(lineno)d) %(message)s')

DBS_PATH = 'groups'
db_temp = ''  # резервная копия базы


class BaseNotFoundError(Exception):
    """
    Исключение, выбрасываемое, если запрашиваемая база не существует
    """
    pass


def add(group, semester='', subject=''):
    """
    ДОБАВИТЬ ГРУППУ И/ИЛИ СЕМЕСТР И/ИЛИ ПРЕДМЕТ
    Принимает:
        group (str или int) - номер группы
        semester (str или int), необязательный - номер группы
        subject (str), необязательный - название предмета
    Возвращает:
        (bool) - успешность операции
    """
    group = str(group)
    semester = str(semester)
    subject = subject.upper()
    if not exists(DBS_PATH):  # если нет папки с группами, создать
        mkdir(DBS_PATH)
    if semester and subject:
        path = DBS_PATH + '/' + group + '/' + semester + '/' + subject
        if not exists(path):
            if not exists(DBS_PATH + '/' + group):  # е. нет папки группы
                mkdir(DBS_PATH + '/' + group)
            if not exists(DBS_PATH + '/' + group + '/' + semester):  # е. нет папки семестра
                mkdir(DBS_PATH + '/' + group + '/' + semester)
                # создать базу со студентами
                with open(DBS_PATH + '/' + group + '/' + semester + '/' + 'students', 'w') as base:
                        base.write(json.dumps({}))
            # создать базу с посещаемостью
            with open(path, 'w') as base:
                base.write(json.dumps({}))
        else:
            logging.warning('Предмет "%s" уже существует'%subject)
            return False
    elif semester and not subject:
        path = DBS_PATH + '/' + group + '/' + semester
        if not exists(path):
            mkdir(path)
            with open(path+'students', 'w') as base:
                base.write(json.dumps({}))
        else:
            logging.warning('Семестр "%s" уже существует'%semester)
            return False
    elif not semester and subject:
        logging.warning('Получен параметр subject, но отсутствует semester')
        return False
    else:
        path = DBS_PATH + '/' + group
        if not exists(path):
            mkdir(path)
        else:
            logging.warning('Группа "%s" уже существует'%group)
            return False
    return True
    # FIXME: оптимизировать код


def get(data=''):
    """
    ПОЛУЧИТЬ СПИСОК ГРУПП/СЕМЕСТРОВ/ПРЕДМЕТОВ
    Принимает:
        data
    Возвращает:
        (list)

    data = '' - список групп
    data = 1 - список семестров
    data = (1, 1) - список предметов
    """
    if not data:
        # е. нет папки с группами, создать её и вернуть пустой список
        if not exists(DBS_PATH):
            mkdir(DBS_PATH)
            return ()
        return listdir(DBS_PATH)
    if isinstance(data, (str, int)):
        group = str(data)
        return listdir(DBS_PATH + '/' + group)
    if isinstance(data, (tuple, list)):
        group = str(data[0])
        semester = str(data[1])
        return listdir(DBS_PATH + '/' + group + '/' + semester)

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
        group (str или int) - номер группы
    Возвращает:
        (list) - список семестров
            (str) - каждый элемент
    """
    group = str(group)
    return listdir(DBS_PATH + '/' + group)


def get_subjects(group, semester):
    """
    ПОЛУЧИТЬ СПИСОК ПРЕДМЕТОВ В СЕМЕСТРЕ
    Принимает:
        group (str или int) - номер группы
        semester (str или int) - номер семестра
    Возвращает:
        (list) - список предметов
            (str) - каждый элемент
    """
    group = str(group)
    semester = str(semester)
    return listdir(DBS_PATH + '/' + group + '/' + semester)


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
        self.subject = subject.upper()
        self.path = DBS_PATH + '/' + self.group + '/' + self.semester + '/' + self.subject
        if not exists(self.path):
            raise BaseNotFoundError('База данных \"%s\" не найдена' % self.path)
        self.base = self._read_db()
        # self.students = self._read_db('students')

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
            if not lesson in self.base['attendance']:
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

    def get_student_info(self, pers_number='', name='', right=False):
        """
        ПОЛУЧИТЬ ИНФОРМАЦИЮ О СТУДЕНТЕ
        """
        pers_number = str(pers_number)
        if pers_number:
            return self.base['students'][pers_number][0] if right else self.base['students'][pers_number][0]
        if name:
            for student in self.base['students']:
                if self.base['students'][student][0] == name:
                    return student
        # TODO

    def get_names(self):
        """
        ПОЛУЧИТЬ СПИСОК СТУДЕНТОВ
        Возвращает:
            (tuple) - список из имён студентов
        """
        return tuple(self.base['students'][student][0] for student in self.base['students'])

    def get_lessons(self):
        """
        ПОЛУЧИТЬ СПИСОК ЗАНЯТИЙ (ДАТЫ) В СЕМЕСТРЕ
        Возвращает:
            (tuple) - список дат занятий
        """
        return tuple(self.base['attendance'].keys())

    def get_values_semester(self):
        """
        ПОЛУЧИТЬ ДАННЫЕ ПО СЕМЕСТРУ (ИМЕНА, ДАТЫ, КОДЫ ПОСЕЩЕНИЙ)
        Возвращает:
            (diсt)

        ПРИМЕР:
            # TODO
        """
        students = {student: self.base['students'][student][0] for student in self.base['students']}
        return {date: {students[student]: self.base['attendance'][date][student] for student in self.base['attendance'][date]} for date in self.base['attendance']}

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
    def _read_db(self, path=''):
        global db_temp
        if not path:
            path = self.path
        base = open(path, 'r').read()
        # REVIEW сохранение базы
        db_temp = base  # создание резервной копии базы в памяти
        return json.loads(base)

    def _save_db(self, path):
        try:
            with open(self.path, 'w') as file:
                file.write(json.dumps(self.base))
        except ValueError:  # в случае возникновения ошибки, записать в файл первоначальный вид базы
            logging.critical('Ошибка с форматом базы')
            with open(self.path, 'w') as base:
                base.write(db_temp)
            logging.warning('Была записана старая версия базы')
            return False
        return True
