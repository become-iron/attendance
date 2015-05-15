# coding: utf-8
"""
Работа с базами данных
"""
import sqlite3
from os.path import exists  # проверка существования файла
from functools import reduce


class WrongDataError(Exception):
    pass


class BaseNotFoundError(Exception):
    pass


# ВНУТРЕННИЕ ФУНКЦИИ
def _query(db, query):
    db = 'groups/' + db
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
    # добавить таблицу
    query = 'CREATE TABLE {table} ({values});'\
        .format(table=table,
                values=reduce(lambda x, y: x+', '+y, values) if isinstance(values, tuple) else values)
    print(query)
    return _query(db=db, query=query)


def _insert(db, table, values):
    # добавить строки
    query = 'INSERT INTO {table} (column1, column2, column3) VALUES {values}'\
        .format(table=table,
                values=str(values)[1:-1])  # FIXME
    return _query(db=db, query=query)


def _select(db, table, values=(), where=''):
    query = 'SELECT {values} FROM {table};'\
        .format(values=reduce(lambda x, y: x+', '+y, values) if values else '*',
                table=table)
    if where:
        query += ' WHERE {where}'.format(where=where)
    query += ';'
    return _query(db=db, query=query)


# ФУНКЦИИ ДЛЯ ВЫЗОВА
def add_group(group):
    """
    Создать новую базу с учебной группой
    Принимает:
        group (str) - номер группы (имя файла базы, если не указано name)
        semester (int) - номер семестра
        date (tuple) - даты занятий
    """
    # date = '_' + reduce(lambda x, y: x + ' TEXT DEFAULT \'0\', _' + y, date) + ' TEXT DEFAULT \'0\''
    # query = 'id INTEGER PRIMARY KEY, name TEXT, {date}'\
    #     .format(date=date)
    query = 'id INTEGER PRIMARY KEY, name TEXT'
    return _create_table(db=group+'.db', table='students', values=query)


def check_in(db, id):
    """
    Отметиться
    """
    pass