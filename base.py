# coding: utf-8
"""

"""
import sqlite3


# РАБОТА С БАЗАМИ ДАННЫХ
def _query(db, data):
    """
    Любой запрос
    """
    try:
        with sqlite3.connect(database=db) as con:
            cur = con.cursor()
            cur.execute(data)
            con.commit()
            return con
    except sqlite3.DatabaseError as error:
        return error


def add_group(group, name=False, path=False):
    """
    Создать новую базу с учебной группой
    Принимает:
        group (str) - номер группы (имя файла базы, если не указано name)
        name (str) - имя файла с базой
        parh (str) - путь к папке с базой, по умолчанию корневая
    """
    query = None
    if name and path:
        _query(db=path+'/'+name, data=query)
    pass

def check_in():
    """
    Отметиться
    """
    pass