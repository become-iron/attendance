# coding: utf-8
import json
from os.path import exists  # проверка существования файла
from os import mkdir, listdir
import logging
from pprint import pprint  # TEMP

logging.basicConfig(format='%(levelname)-7s:[#%(lineno)d] %(message)s')

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
    if not exists(DBS_PATH):  # е. нет папки с группами, создать
        mkdir(DBS_PATH)
        with open(DBS_PATH + '/' + 'superusers', 'w') as base:
            base.write(json.dumps({}))
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
            logging.warning('Предмет "%s" уже существует' % subject)
            return False
    elif semester and not subject:
        path = DBS_PATH + '/' + group + '/' + semester
        if not exists(path):
            mkdir(DBS_PATH + '/' + group)
            mkdir(path)
            # создать базу со студентами
            with open(path+'/students', 'w') as base:
                base.write(json.dumps({}))
        else:
            logging.warning('Семестр "%s" уже существует' % semester)
            return False
    elif not semester and subject:
        logging.warning('Получен параметр subject, но отсутствует semester')
        return False
    else:
        path = DBS_PATH + '/' + group
        if not exists(path):
            mkdir(path)
        else:
            logging.warning('Группа "%s" уже существует' % group)
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
    data = <группа> - список семестров
    data = (<группа>, <семестр>) - список предметов
    """
    if not data:  # список групп
        # е. нет папки с группами, вернуть пустой список
        if not exists(DBS_PATH):
            return ()
        return listdir(DBS_PATH)
    if isinstance(data, (str, int)):  # список семестров
        group = str(data)
        return listdir(DBS_PATH + '/' + group)
    if isinstance(data, (tuple, list)):  # список предметов
        group = str(data[0])
        semester = str(data[1])
        semesters_list = listdir(DBS_PATH + '/' + group + '/' + semester)
        semesters_list.remove('students')
        return semesters_list
    logging.error('Переданы некорректные данные')
    return False


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
        self.attendance = self._read_db()

        self.path_s = DBS_PATH + '/' + self.group + '/' + self.semester + '/' + 'students'
        self.students = self._read_db(self.path_s)

        self.path_su = DBS_PATH + '/' + 'superusers'
        self.superusers = self._read_db(self.path_su)

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
            Коды прав студентов:
            0 - обычный пользователь
            1 - повышенные права
        Возвращает:
            (bool) - успешность операции
        """
        for student in students:
            try:
                right = student[2]
            except IndexError:
                right = 0
            if student[0] not in self.students:  # е. студента нет ещё в базе (по таб. номеру)
                self.students.update({str(student[0]): (student[1], right)})
                for date in self.get_lessons():  # заполнение посещаемости нулями
                    self.check_in(date, student[0], 0)
            else:
                logging.warning('Этот таб. номер уже есть в базе ({}, {})'.format(student[0], student[1]))
        return True if self._save_db(path=self.path_s, base=self.students) else False

    def add_superuser(self, login, password):
        """
        ДОБАВИТЬ СУПЕРПОЛЬЗОВАТЕЛЯ
        """
        login = str(login)
        password = str(password)
        if login not in self.superusers:
            self.superusers.update({login: password})
            self._save_db(path=self.path_su, base=self.superusers)
            return True
        logging.warning('Пользователь "%s" уже есть' % login)
        return False

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
            if lesson not in self.attendance:  # е. такой даты ещё нет
                self.attendance.update({lesson: {}})
                for student in self.students.keys():  # заполнение посещаемости нулями
                    self.check_in(lesson, student, 0)
            else:
                logging.warning('Дата %s уже есть в базе' % lesson)
        return True if self._save_db() else False

    def update_student(self, data, pers_number='', name='', right=''):
        """
        ОБНОВИТЬ ДАННЫЕ СТУДЕНТА
        Принимает:
            data (str или int)
            pers_number
            name
            right
        """
        if right:
            if pers_number:
                pass
            elif name:
                pass
            else:
                logging.error('Указан параметр right, но не получен pers_number или name')
                return False
        elif pers_number:
            pass
        elif name:
            pers_number = self.get_student_info(name=name)
            right = self.get_student_info(name=name, right=True)
            if not pers_number:
                logging.error('Студент %s не найден' % name)
                return False
            self.students.update({pers_number: (data, right)})
        else:
            logging.warning('Не был передан ни один параметр')
            return False
        return True if self._save_db(path=self.path_s, base=self.students) else False

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
        if pers_number in self.students and date in self.attendance:
            self.attendance[date].update({pers_number: code})
            return True if self._save_db() else False
        else:
            logging.warning('Таб. номер {} или дата {} не найдены'.format(pers_number, date))
            return False

    def get_student_info(self, pers_number='', name='', right=False):
        """
        ПОЛУЧИТЬ ИНФОРМАЦИЮ О СТУДЕНТЕ
        """
        pers_number = str(pers_number)
        if pers_number:
            try:
                return self.students[pers_number][0] if right else self.students[pers_number][0]
            except IndexError:
                logging.error('Студент не найден')
                return False
        if name:
            for student in self.students:
                if self.students[student][0] == name:
                    return self.students[student][1] if right else student
            logging.error('Студент не найден')
            return False

    def get_names(self):
        """
        ПОЛУЧИТЬ СПИСОК СТУДЕНТОВ (ИМЕНА)
        Возвращает:
            (tuple) - список из имён студентов
        """
        return tuple(self.students[student][0] for student in self.students)

    def get_lessons(self):
        """
        ПОЛУЧИТЬ СПИСОК ЗАНЯТИЙ (ДАТЫ) В СЕМЕСТРЕ
        Возвращает:
            (tuple) - список дат занятий
        """
        return tuple(self.attendance.keys())

    def get_values_semester(self):
        """
        ПОЛУЧИТЬ ДАННЫЕ ПО СЕМЕСТРУ (ИМЕНА, ДАТЫ, КОДЫ ПОСЕЩЕНИЙ)
        Возвращает:
            (diсt)

        ПРИМЕР:
            # TODO
        """
        students = {student: self.students[student][0] for student in self.students}
        return {date: {students[student]: self.attendance[date][student] for student in self.attendance[date]} for date in self.attendance}

    def verify(self, login, password):
        """
        ВЕРИФИКАЦИЯ ДАННЫХ СУПЕРПОЛЬЗОВАТЕЛЯ
        Принимает:
            login - (str или int) - логин
            password (str или int) - пароль
        Возвращает:
            (bool) - верность данных
        """
        login = str(login)
        password = str(password)
        if login in self.superusers:
            return self.superusers[login] == password
        logging.warning('Логин "%s" не найден' % login)
        return False

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

    def _save_db(self, path='', base=''):
        if not path:
            path = self.path
            base = self.attendance
        try:
            with open(path, 'w') as file:
                file.write(json.dumps(base))
        except ValueError:  # в случае возникновения ошибки, записать в файл первоначальный вид базы
            logging.critical('Ошибка с форматом базы')
            with open(path, 'w') as base:
                base.write(db_temp)
            logging.warning('Была записана старая версия базы')
            return False
        return True
