# -*- coding: utf-8 -*-

import random
import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

import logic

error_id = None
semester_name = None
group_name = None

class MainDialog(QtGui.QWidget):
    def __init__(self):
        global choose_container, main_widget, choose_gb
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Контроль посещаемости')

        # создание сетки, в которую помещаются остальные виджеты
        main_container = QtGui.QGridLayout(self)

        # создание кнопки для выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        main_container.addWidget(self.exit_button, 2, 0, 1, 1)

        # создание кнопки для ввода данных
        self.open_button = QtGui.QPushButton(u"Открыть")
        self.connect(self.open_button, QtCore.SIGNAL('clicked()'), self.open)
        main_container.addWidget(self.open_button, 1, 0, 1, 1)

        # создание рамки для ввода id
        choose_gb = QtGui.QGroupBox('Выберите группу и семестр', self)
        choose_gb.setAlignment(QtCore.Qt.AlignCenter)

        # добавление рамки в сетку
        main_container.addWidget(choose_gb, 0, 0, 1, 1)

        # создание сетки, в которую помещаются выпадающие списки
        choose_container = QtGui.QGridLayout(choose_gb)

        # создание сообщения о выборе группы
        choose_group_l = QtGui.QLabel(u"""Выберите номер группы:""", choose_gb)
        choose_container.addWidget(choose_group_l, 0, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_group_cb = QtGui.QComboBox(choose_gb)
        choose_group_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        choose_group_cb.addItem(None)

        """
        Вызываю функцию для получения списка групп
        """
        list_of_groups = logic.group_get()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            choose_group_cb.addItem(str(i))
        choose_group_cb.setEditable(True)

        # добавление списка в сетку
        choose_container.addWidget(choose_group_cb, 1, 0, 1, 1)

        # при выборе значения из списка вызывает функцию по поиску семестров
        choose_group_cb.currentIndexChanged[str].connect(self.choose_semester)

    def choose_semester(self, group_index):
        global choose_container, choose_semester_cb, choose_semester_l, group_name, semester_name
        group_name = group_index

        # семестр обнуляется
        semester_name = None
        print(group_name)
        try:
            choose_semester_l.deleteLater()
            choose_semester_l.setParent(None)
            choose_semester_cb.deleteLater()
            choose_semester_cb.setParent(None)
        except NameError:
            pass
        except RuntimeError:
            pass

        # создание сообщения о выборе группы
        choose_semester_l = QtGui.QLabel(u"""Выберите номер семестра:""", choose_gb)
        choose_container.addWidget(choose_semester_l, 3, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_semester_cb = QtGui.QComboBox(choose_gb)
        choose_semester_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        choose_semester_cb.addItem(None)

        """
        Вызываю функцию для получения списка семестров
        Оправляю номер группы
        Должен получить список с семестрами
        """
        try:
            list_of_semester = logic.semester_get(group_name)
            # добавляет в выпадающий список семестры
            for i in list_of_semester:
                choose_semester_cb.addItem(str(i))
        except logic.WrongDataError:
            try:
                choose_semester_l.deleteLater()
                choose_semester_l.setParent(None)
                choose_semester_cb.deleteLater()
                choose_semester_cb.setParent(None)
            except NameError:
                pass

            choose_gb.resize(choose_gb.sizeHint())
            self.adjustSize()

        choose_semester_cb.setEditable(True)

        # добавление списка в сетку
        choose_container.addWidget(choose_semester_cb, 4, 0, 1, 1)

        # при выборе значения из списка вызывает функцию по поиску семестров
        choose_semester_cb.currentIndexChanged[str].connect(self.semester)

    def semester(self, semester_index):
        global semester_name
        semester_name = semester_index
        print(semester_name)

    def open(self):
        global error_id
        # код ошибки обнуляется
        error_id = None

        if bool(semester_name) is False:
            error_id = 1
            if bool(group_name) is False:
                error_id = 0
        if error_id is not None:
            # если ошибка возникла, окрывается окно с ошибкой
            self.error_window()
        else:
            self.show_table()

    def error_window(self):
        em = ErrorMessage(error_id)
        em.show()
        em.exec_()

    def show_table(self):
        print(group_name, semester_name)


class ErrorMessage(QtGui.QMessageBox):
    def __init__(self, error_id):
        QtGui.QMessageBox.__init__(self)

        # в зависимости от кода надпись меняется
        if error_id == 0:
            self.setText(u"Группа не выбрана")
        elif error_id == 1:
            self.setText(u"Семестр не выбран")

        # настройки окна
        self.setWindowTitle('Ошибка')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.addButton('ОК', QtGui.QMessageBox.AcceptRole)


if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainDialog()
    main.show()
    sys.exit(app.exec_())
