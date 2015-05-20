# coding: utf-8
"""
Работа с базами данных
"""
import sqlite3
from os.path import exists  # проверка существования файла
from os import mkdir, listdir
from functools import reduce

DBS_PATH = 'groups'  # где хранить все базы


class WrongDataError(Exception):
    pass


class BaseNotFoundError(Exception):
    """
    Исключение, выбрасываемое, если запрашиваемая база не существует
    """
    pass


def get_list_of_groups():
    """
    ПОЛУЧИТЬ СПИСОК ГРУПП
    Возвращает:
        (tuple) - список групп
            (str) - каждый элемент
        Пример: ('2342', '3244, 'и3242')
    """
    return tuple(map(lambda x: x.replace('.db', ''), listdir(DBS_PATH)))


def add_group(group, students):
    """
    СОЗДАТЬ НОВУЮ БАЗУ С УЧЕБНОЙ ГРУППОЙ
    Принимает:
        group (str) - номер группы (имя файла базы)
        semester (str)
        students (tuple) - ((таб.номер, имя), ..., ...)
    """
    # date = '_' + reduce(lambda x, y: x + ' TEXT DEFAULT \'0\', _' + y, date) + ' TEXT DEFAULT \'0\''
    # query = 'id INTEGER PRIMARY KEY, name TEXT, {date}'\
    #     .format(date=date)
    group = group + '.db'
    query = 'pers_number TEXT, name TEXT'
    _ = _create_table(db=group, table='students', values=query)
    if _ is not True:
        # TODO: удалить базу
        return _
    for student in students:
        _ = _insert(db=group, table='students', columns='pers_number, name', values=student[0] + ', ' + student[1])
        if _ is not True:
            return _
    return True


def add_semester(group, semester, lessons):
    """
    ДОБАВИТЬ СЕМЕСТР
    """
    query = ''
    return _create_table(db=group, table=semester, values=query)


def check_in(db, id):
    """
    Отметиться
    """
    pass


def get_group(db, table, ):
    """
    """
    query = ''
    return _select(db=db, table=table, values='name', order_by='name')


# ВНУТРЕННИЕ ФУНКЦИИ
def _format_data(data, c=-1):
    if c == 0:
        return


def _query(db, query):
    print(query)
    if DBS_PATH:
        if not exists(DBS_PATH):
            mkdir(DBS_PATH)
        db = DBS_PATH + '/' + db
    if not exists(db) and not query.startswith('CREATE TABLE'):
        raise BaseNotFoundError('База данных {} не была найдена'.format(db))
    try:
        con = sqlite3.connect(database=db)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        if query.startswith('SELECT'):
            value = cur.fetchall()
        cur.close()
        con.close()
        return True if not query.startswith('SELECT') else value
    # except sqlite3.Error as error:
    #     return 'Возникла ошибка: {}'.format(error)  # TODO: удалять новосозданную базу, если произошла ошибка
    except UnicodeDecodeError:
        pass


def _create_table(db, table, values):
    # добавить таблицу в базу данных
    query = 'CREATE TABLE {table} ({values});'\
        .format(table=table,
                # values=reduce(lambda x, y: x+', '+y, values) if isinstance(values, tuple) else values)
                 values=values)
    return _query(db=db, query=query)


def _insert(db, table, columns, values):
    # добавить значения в таблицу
    query = 'INSERT INTO {table} VALUES ({values});'\
        .format(table=str(table),
                columns=columns,
                values=values)
    return _query(db=db, query=query)


def _select(db, table, values=(), where='', order_by=''):
    # выбрать значения из таблицы
    query = 'SELECT {values} FROM {table}'\
        .format(values=reduce(lambda x, y: x+', '+y, values) if values else '*',
                table=table)
    if where:
        query += ' WHERE {where}'.format(where=where)
    if order_by:
        query += ' ORDER BY {order_by}'.format(order_by=order_by)
    query += ';'
    return _query(db=db, query=query)
